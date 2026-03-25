import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
import sys

# Add backend to path to allow importing modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from rag import answer_question, load_vector_db
from graph import get_top_persons, get_graph_data_for_visualization

# Setup UI page configuration
st.set_page_config(
    page_title="AI Knowledge Graph Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Injection
st.markdown("""
    <style>
        .main {
            background-color: #0f111a;
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3 {
            color: #f8fafc;
            font-weight: 700;
        }
        h1 {
            background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem !important;
            padding-bottom: 20px;
        }
        .stButton button {
            background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
            transform: translateY(-2px);
        }
        .stTextInput input, .stTextArea textarea {
            background-color: #1e2130 !important;
            color: white !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 8px;
        }
        .metric-card {
            background: rgba(30, 33, 48, 0.6);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            margin-bottom: 1rem;
        }
        .answer-box {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            border-left: 4px solid #8b5cf6;
            padding: 1.5rem;
            border-radius: 8px;
            font-size: 1.1rem;
            line-height: 1.6;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("<h1>🧠 AI Knowledge Graph Dashboard</h1>", unsafe_allow_html=True)
st.markdown("Query the Enron dataset through an advanced Retrieval-Augmented Generation (RAG) and Neo4j Knowledge Graph system.")

# Initialize session state for initial loading
if 'db_loaded' not in st.session_state:
    with st.spinner("Initializing FAISS Vector DB Space..."):
        # We assume dataset is created. We load it
        st.session_state.db_loaded = load_vector_db()

# Layout layout
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown("### 🔍 Query Engine")
    
    query = st.text_input("Ask a question about the emails or entities:", placeholder="e.g. Who is discussing energy trading?")
    
    if st.button("Generate Answer ✨"):
        if not query:
            st.warning("Please enter a query.")
        else:
            with st.spinner("Retrieving contexts & Generating AI insights..."):
                response = answer_question(query)
                answer = response.get("answer", "No answer found.")
                emails = response.get("retrieved_emails", [])
                graph_rels = response.get("retrieved_graph", [])
                
                st.markdown("### 💡 Final Answer")
                st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

                st.markdown("### 📄 Retrieved Context")
                tab1, tab2 = st.tabs(["📧 Top Emails (FAISS)", "🕸️ Graph Relationships (Neo4j)"])
                
                with tab1:
                    if emails:
                        for i, email in enumerate(emails):
                            with st.expander(f"Email Document #{i+1}"):
                                st.write(email)
                    else:
                        st.info("No emails retrieved.")
                
                with tab2:
                    if graph_rels:
                        for idx, rel in enumerate(graph_rels):
                            st.write(f"- {rel}")
                    else:
                        st.info("No relevant graph relationships found for query entities.")

with col_right:
    st.markdown("### 📊 Knowledge Graph Analytics")
    
    # Render Network
    st.markdown("**Entity Relationship Network (Sample)**")
    
    # Generate pyvis graph dynamically
    nodes, edges = get_graph_data_for_visualization(limit=50)
    
    if len(nodes) > 0:
        net = Network(height="400px", width="100%", bgcolor="#1e2130", font_color="white", select_menu=True)
        # Add nodes
        for node, lbl in nodes:
            color = "#3b82f6" if lbl == "PERSON" else "#10b981" if lbl == "ORG" else "#f59e0b"
            net.add_node(node, label=node, title=lbl, color=color, shape="dot", size=20)
        # Add edges
        for src, tgt in edges:
            net.add_edge(src, tgt, title="RELATED_TO", color="#4b5563")
            
        net.repulsion(node_distance=150, central_gravity=0.2, spring_length=150, spring_strength=0.05, damping=0.95)
        
        try:
            path = "temp_graph.html"
            net.save_graph(path)
            with open(path, "r", encoding="utf-8") as f:
                html_data = f.read()
            components.html(html_data, height=410)
        except Exception as e:
            st.error(f"Graph rendering error: {e}")
    else:
        st.info("No graph data available. Please ensure Neo4j is connected and populated.")

    st.markdown("---")
    
    # Top 10 Actors
    st.markdown("**🏆 Top 10 Most Frequent Entities (PERSON)**")
    with st.spinner("Aggregating Neo4j Graph..."):
        top_persons = get_top_persons(limit=10)
        
        if top_persons:
            # Display visually as cards
            for i, p in enumerate(top_persons):
                st.markdown(f"""
                <div style='background: rgba(30,33,48,0.5); padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #3b82f6; display: flex; justify-content: space-between;'>
                    <span style='color:#e2e8f0; font-weight: 500;'>#{i+1} {p['name'].title()}</span>
                    <span style='color:#94a3b8; font-size: 0.9em;'>{p['connections']} connections</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Could not retrieve top persons. Ensure graph is populated.")
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8em; padding-top: 20px;'>Build by <b>Charan Karthik</b></div>", unsafe_allow_html=True)
