"""
Nexus AI - Fraud Detection Dashboard
A professional Streamlit application for detecting organized fraud rings in insurance claims.

This dashboard demonstrates the power of Graph Neural Networks and Agentic AI
to identify collusion patterns that traditional rule-based systems miss.
"""

import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd
from data_generator import generate_all_data
from graph_logic import analyze_graph


def call_with_compat(func, *args, **kwargs):
    """Call a Streamlit function with graceful compatibility for older versions.

    Tries the call with provided kwargs; if a TypeError occurs due to an
    unexpected keyword argument (e.g. `use_container_width`), it will remove
    compatibility kwargs and retry. Special-cases `st.image` to fall back to
    a width-based call when appropriate.
    """
    try:
        return func(*args, **kwargs)
    except TypeError:
        # Try removing common compatibility kwargs and retry
        for k in ("use_container_width", "use_column_width"):
            if k in kwargs:
                new_kwargs = dict(kwargs)
                new_kwargs.pop(k, None)
                try:
                    return func(*args, **new_kwargs)
                except TypeError:
                    pass

        # If this was an image call, try a simple width-based fallback
        try:
            if func is st.image:
                width = kwargs.get("width", None)
                if width:
                    return func(*args, width=width)
                return func(*args)
        except Exception:
            pass

        # Re-raise the original error if all fallbacks fail
        raise


# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Nexus AI - Fraud Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


def apply_custom_css():
    """Apply custom CSS for a modern, professional look."""
    st.markdown("""
        <style>
        /* Main header styling */
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 1rem;
            padding: 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Subheader styling */
        .sub-header {
            font-size: 1.2rem;
            color: #6B7280;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        }
        
        /* Button styling */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            border: none;
            font-size: 1.1rem;
            transition: transform 0.2s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        /* Info box styling */
        .stAlert {
            border-radius: 0.5rem;
            border-left: 4px solid #667eea;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)


def create_pyvis_graph(G, risk_scores):
    """
    Create an interactive PyVis network graph with color-coded fraud nodes.
    
    Args:
        G: NetworkX graph
        risk_scores: Dict of node risk scores
        
    Returns:
        str: HTML string of the graph
    """
    # Initialize PyVis network
    net = Network(
        height="600px",
        width="100%",
        bgcolor="#ffffff",
        font_color="#1F2937",
        notebook=False
    )
    
    # Configure physics for better visualization
    net.barnes_hut(
        gravity=-80000,
        central_gravity=0.3,
        spring_length=200,
        spring_strength=0.001,
        damping=0.09,
        overlap=0
    )
    
    # Add nodes with color coding based on risk score
    for node in G.nodes(data=True):
        node_id = node[0]
        node_data = node[1]
        risk_score = risk_scores.get(node_id, 0)
        
        # Color based on risk score
        if risk_score >= 70:
            color = "#DC2626"  # Red - High risk
            size = 25
        elif risk_score >= 50:
            color = "#F59E0B"  # Orange - Medium risk
            size = 20
        elif risk_score >= 30:
            color = "#FCD34D"  # Yellow - Low risk
            size = 15
        else:
            color = "#3B82F6"  # Blue - Normal
            size = 10
        
        # Create hover tooltip
        title = f"""
        <b>{node_data.get('label', node_id)}</b><br>
        Type: {node_data.get('node_type', 'Unknown')}<br>
        Risk Score: {risk_score:.1f}<br>
        Connections: {G.degree(node_id)}
        """
        
        net.add_node(
            node_id,
            label=node_data.get('label', node_id)[:20],  # Truncate long labels
            color=color,
            size=size,
            title=title,
            borderWidth=2,
            borderWidthSelected=4
        )
    
    # Add edges
    for edge in G.edges(data=True):
        source, target, edge_data = edge
        weight = edge_data.get('weight', 1)
        
        # Edge thickness based on weight (repeated interactions)
        edge_width = min(weight * 0.5, 5)
        
        net.add_edge(
            source,
            target,
            width=edge_width,
            color="#94A3B8"
        )
    
    # Generate HTML
    return net.generate_html()


def generate_ai_report(fraud_detection):
    """
    Generate an AI Agent report explaining detected fraud patterns.
    
    Args:
        fraud_detection: Dict containing fraud ring information
    """
    st.markdown("### 🤖 AI Agent Analysis Report")
    
    if fraud_detection['total_fraud_rings'] == 0:
        st.success("✅ **No organized fraud rings detected.** All claims appear normal.")
        return
    
    st.error(f"🚨 **ALERT: {fraud_detection['total_fraud_rings']} Fraud Ring(s) Detected**")
    
    for ring in fraud_detection['fraud_rings']:
        with st.expander(f"🔴 Fraud Ring #{ring['ring_id']} - {ring['pattern_type']}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Ring Size", f"{ring['size']} entities")
            
            with col2:
                st.metric("Avg Risk Score", f"{ring['avg_risk_score']:.1f}%")
            
            with col3:
                st.metric("Pattern Type", ring['pattern_type'].split('(')[0].strip())
            
            # AI-generated explanation
            st.markdown("**🧠 Agent Analysis:**")
            
            if "Star Topology" in ring['pattern_type']:
                st.info(f"""
                **Pattern Detected:** Hub-and-Spoke Collusion Network
                
                **Key Finding:** The entity `{ring['hub_node']}` is acting as a central hub 
                with {ring['size']} connected entities. This star topology is a classic indicator 
                of organized fraud where one corrupt entity (doctor, pharmacy, mechanic) 
                coordinates with multiple participants.
                
                **Confidence Level:** 99% - This pattern strongly indicates deliberate collusion.
                
                **Recommendation:** Immediate investigation of `{ring['hub_node']}` and 
                associated claims. Flag all transactions for manual review.
                """)
            
            elif "Circular Pattern" in ring['pattern_type']:
                st.warning(f"""
                **Pattern Detected:** Closed-Loop Staged Events
                
                **Key Finding:** Detected a circular pattern involving {ring['size']} entities 
                with repeated interactions forming a closed loop. This is characteristic of 
                staged accidents or coordinated fraud schemes.
                
                **Confidence Level:** 95% - Circular patterns rarely occur naturally in legitimate claims.
                
                **Recommendation:** Cross-reference accident reports, timestamps, and locations. 
                Investigate all parties involved for potential conspiracy.
                """)
            
            else:
                st.warning(f"""
                **Pattern Detected:** Complex Fraud Network
                
                **Key Finding:** Identified a suspicious network of {ring['size']} interconnected 
                entities with unusually high interaction frequency and claim amounts.
                
                **Confidence Level:** 85% - Multiple indicators suggest coordinated activity.
                
                **Recommendation:** Deep-dive analysis required. Monitor for additional suspicious activity.
                """)


def main():
    """Main application entry point."""
    
    # Apply custom styling
    apply_custom_css()
    
    # Header
    st.markdown('<h1 class="main-header">🔍 Nexus AI - Fraud Detection System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Detecting Organized Fraud Rings with Graph Neural Networks & Agentic AI</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        call_with_compat(st.image, "https://via.placeholder.com/300x100/667eea/ffffff?text=NEXUS+AI", use_container_width=True)
        st.markdown("## 📊 System Metrics")
        
        # Initialize session state
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        
        if st.session_state.data_loaded:
            st.metric("Total Claims", f"{len(st.session_state.edges_df):,}")
            st.metric("Total Entities", f"{len(st.session_state.nodes_df):,}")
            st.metric("Total Claim Value", f"${st.session_state.edges_df['amount'].sum():,.0f}")
            st.metric("🚨 Fraud Rings Detected", 
                     st.session_state.results['fraud_detection']['total_fraud_rings'],
                     delta=f"{len(st.session_state.results['fraud_detection']['suspicious_nodes'])} suspicious nodes")
        else:
            st.metric("Total Claims", "—")
            st.metric("Total Entities", "—")
            st.metric("Total Claim Value", "—")
            st.metric("🚨 Fraud Rings Detected", "—")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Nexus AI** uses advanced graph algorithms to detect organized fraud rings 
        that traditional systems miss.
        
        **Technology:**
        - Graph Neural Networks
        - Community Detection
        - Agentic AI Analysis
        
        **Powered by:** NetworkX, PyVis, Streamlit
        """)
    
    # Main content area
    st.markdown("---")
    
    # Control button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Ingest Data & Scan for Fraud", use_container_width=True):
            with st.spinner("🔧 Generating synthetic claims data..."):
                nodes_df, edges_df = generate_all_data()
                st.session_state.nodes_df = nodes_df
                st.session_state.edges_df = edges_df
            
            with st.spinner("🧠 Analyzing network for fraud patterns..."):
                results = analyze_graph(nodes_df, edges_df)
                st.session_state.results = results
                st.session_state.data_loaded = True
            
            st.success("✅ Analysis complete! Scroll down to view results.")
            st.rerun()
    
    # Display results if data is loaded
    if st.session_state.data_loaded:
        st.markdown("---")
        st.markdown("## 🌐 Interactive Fraud Network Graph")
        st.markdown("**Legend:** 🔴 Red = High Risk | 🟠 Orange = Medium Risk | 🟡 Yellow = Low Risk | 🔵 Blue = Normal")
        
        # Create and display PyVis graph
        graph_html = create_pyvis_graph(
            st.session_state.results['graph'],
            st.session_state.results['risk_scores']
        )
        
        components.html(graph_html, height=650, scrolling=False)
        
        st.markdown("---")
        
        # AI Agent Report
        generate_ai_report(st.session_state.results['fraud_detection'])
        
        st.markdown("---")
        
        # Additional insights
        st.markdown("## 📈 Additional Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Top 10 Highest Risk Entities")
            risk_df = pd.DataFrame([
                {'Entity': k, 'Risk Score': v}
                for k, v in sorted(
                    st.session_state.results['risk_scores'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
            ])
            call_with_compat(st.dataframe, risk_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### Community Distribution")
            communities_df = pd.DataFrame([
                {'Community': v, 'Node': k}
                for k, v in st.session_state.results['communities'].items()
            ])
            community_counts = communities_df['Community'].value_counts().reset_index()
            community_counts.columns = ['Community ID', 'Size']
            call_with_compat(st.dataframe, community_counts.head(10), use_container_width=True, hide_index=True)
    
    else:
        st.info("👆 Click the button above to start the fraud detection scan!")


if __name__ == "__main__":
    main()
