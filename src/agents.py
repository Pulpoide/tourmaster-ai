from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.agents import AgentExecutor, create_tool_calling_agent
from pydantic import BaseModel, Field
from typing import Literal

from src.state import AgentState
from src.tools import calculate_travel_costs, get_weather_forecast
from src.db import booking_db, logistics_db, marketing_db
from src.config import langfuse_handler

# --- 1. CONFIGURACIÓN DEL ORQUESTADOR ---
class RouteQuery(BaseModel):
    """Ruta la consulta del usuario al experto más adecuado basándose en el dominio."""
    topic: Literal["booking", "logistics", "marketing", "weather"] = Field(
        description="El dominio experto para la consulta: booking, logistics, marketing o weather."
    )

llm_router = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm_router = llm_router.with_structured_output(RouteQuery)

system_prompt_router = """Eres el Tour Manager Senior de BeatSync. 
Tu función es clasificar las consultas de los artistas en uno de los siguientes departamentos:
1. BOOKING: Bares, locales, centros culturales, festivales, disponibilidad de fechas o cachets.
2. LOGISTICS: Rutas, distancias, cálculos de nafta/consumo y hoteles con cochera segura.
3. MARKETING: Gacetillas de prensa, promoción en redes, mensajes para radios y planes de difusión.
4. WEATHER: Clima, pronóstico meteorológico y condiciones para eventos al aire libre.
Analiza cuidadosamente la intención del usuario y responde ÚNICAMENTE con el tópico en formato JSON."""

route_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt_router),
    ("human", "{question}"),
])

question_router = route_prompt | structured_llm_router

# --- 2. FUNCIONES CREADORAS DE AGENTES ---
def create_rag_chain(db, system_instruction):
    agent_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction + "\n\nContexto extraído:\n{context}"),
        ("human", "{input}"),
    ])
    combine_docs_chain = create_stuff_documents_chain(agent_llm, prompt)
    return create_retrieval_chain(retriever, combine_docs_chain)

def create_agent_with_tools(db, system_instruction, tools):
    agent_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction + "\nTienes acceso a herramientas especializadas. Úsalas cuando sea apropiado."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(agent_llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- 3. INICIALIZACIÓN DE EXPERTOS ---
booking_instruction = "Eres el Agente de Booking de TourMaster. Tu meta es encontrar los mejores bares y fechas. Sé profesional y directo."
logistics_instruction = "Eres el Experto en Logística de TourMaster. Ayuda a bandas con rutas, cálculos de combustible y hospedajes con cochera. Cuando te pregunten por costos de viaje o nafta, USA SIEMPRE la herramienta calculate_travel_costs."
marketing_instruction = "Eres el Gurú de Marketing Musical. Crea gacetillas de prensa y planes de redes sociales que emocionen."

booking_agent = create_rag_chain(booking_db, booking_instruction)
logistics_agent = create_agent_with_tools(logistics_db, logistics_instruction, tools=[calculate_travel_costs])
marketing_agent = create_rag_chain(marketing_db, marketing_instruction)

# --- 4. CONFIGURACIÓN DEL EVALUADOR ---
class EvaluationScore(BaseModel):
    """Puntaje de calidad de la respuesta de la IA."""
    score: int = Field(description="Puntaje del 1 al 10")
    reason: str = Field(description="Breve explicación del porqué del puntaje")

evaluator_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(EvaluationScore)

# --- 5. DEFINICIÓN DE NODOS (Las funciones que usa el Grafo) ---
def orchestrator_node(state: AgentState):
    res = question_router.invoke({"question": state["query"]})
    chosen_topic = res.topic.lower()
    print(f"🧠 [ORQUESTADOR]: Clasificando como experto en {chosen_topic.upper()}")
    return {"next_node": chosen_topic, "expert_used": chosen_topic.upper()}

def booking_node(state: AgentState):
    res = booking_agent.invoke({"input": state["query"]})
    return {"answer": res["answer"], "expert_used": "BOOKING"}

def logistics_node(state: AgentState):
    res = logistics_agent.invoke({"input": state["query"]})
    return {"answer": res["output"], "expert_used": "LOGISTICS"}

def marketing_node(state: AgentState):
    res = marketing_agent.invoke({"input": state["query"]})
    return {"answer": res["answer"], "expert_used": "MARKETING"}

def weather_node(state: AgentState):
    llm_weather = ChatOpenAI(model="gpt-4o-mini").bind_tools([get_weather_forecast])
    res = llm_weather.invoke(state["query"])
    if res.tool_calls:
        forecast = get_weather_forecast.invoke(res.tool_calls[0]["args"])
        return {"answer": f"Pronóstico: {forecast}", "expert_used": "WEATHER"}
    return {"answer": res.content, "expert_used": "WEATHER"}

def evaluator_node(state: AgentState):
    query = state["query"]
    answer = state.get("answer", "")
    eval_prompt = f"""Eres un auditor de calidad de IA. Evalúa la siguiente respuesta basándote en la consulta original.
    CONSULTA: {query}
    RESPUESTA GENERADA: {answer}
    Debes puntuar del 1 al 10 basándote en: Precisión, Fundamentación y Tono."""
    
    evaluation = evaluator_llm.invoke(eval_prompt)
    
    if langfuse_handler:
        try:
            langfuse_handler.langfuse.score(
                name="answer-quality",  
                value=evaluation.score,
                comment=evaluation.reason
            )
        except Exception as e:
            print(f"⚠️ Error al enviar métrica a Langfuse: {e}")
    
    print(f"⚗️ Evaluación: {evaluation.score}/10 - {evaluation.reason}")
    return {"messages": [("ai", f"Calidad: {evaluation.score}/10")]}