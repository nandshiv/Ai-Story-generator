import streamlit as st
import time
from story_generator import load_generator, generate_stories

# Page configuration
st.set_page_config(
    page_title="AetherStory AI | Creative Text Generator",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS for premium glassmorphism and modern gradient design
st.markdown("""
<style>
    /* Import modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at 80% 20%, #1e1b30 0%, #0c0a12 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Header design */
    .header-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        background: linear-gradient(180deg, rgba(167, 139, 250, 0.05) 0%, rgba(0,0,0,0) 100%);
        border-radius: 24px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.02);
    }
    
    .gradient-title {
        background: linear-gradient(135deg, #a78bfa 0%, #db2777 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 3.2rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
    }
    
    .header-subtitle {
        color: #9ca3af;
        font-size: 1.15rem;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.5;
    }
    
    /* Custom Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b090f !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-family: 'Outfit', sans-serif;
        color: #a78bfa;
        font-size: 1.4rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.5rem;
        margin-bottom: 1.2rem;
    }
    
    /* Glassmorphic Cards for Stories */
    .story-card {
        background: rgba(255, 255, 255, 0.025);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
        margin-bottom: 24px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .story-card:hover {
        transform: translateY(-4px);
        border-color: rgba(167, 139, 250, 0.3);
        box-shadow: 0 16px 48px 0 rgba(167, 139, 250, 0.08);
    }
    
    .story-header {
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #a78bfa;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 0.5rem;
    }
    
    .story-prompt-highlight {
        color: #f472b6;
        font-weight: 600;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .story-body {
        color: #e5e7eb;
        font-size: 1.05rem;
        line-height: 1.65;
        font-weight: 300;
    }
    
    /* Preset Button Styling */
    .preset-btn {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 10px 16px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 10px;
    }
    
    .preset-btn:hover {
        background: rgba(167, 139, 250, 0.1);
        border-color: rgba(167, 139, 250, 0.3);
    }
    
    /* Quick badge style */
    .tag-badge {
        background: rgba(167, 139, 250, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.2);
        color: #c084fc;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE & CACHING -----------------

# Load model pipeline using caching so it only happens once
@st.cache_resource(show_spinner=False)
def get_generator():
    try:
        return load_generator("gpt2")
    except Exception as e:
        st.error(f"Error loading Model: {e}")
        return None

# Initialize state for custom prompt
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = "In the year 2050, robots started"

# Preset callbacks
def apply_preset(genre):
    base = "In the year 2050, robots started"
    if genre == "space":
        st.session_state.prompt_input = f"{base} exploring the distant edges of our galaxy. The crewless starship Odyssey-X was the first to detect"
    elif genre == "horror":
        st.session_state.prompt_input = f"{base} to exhibit strange, unauthorized behaviors at night. Owners reported that their household assistants would stand motionless in corners, whispering"
    elif genre == "motivational":
        st.session_state.prompt_input = f"{base} assisting humans in physical tasks, enabling humanity to dedicate themselves to science, art, and healing. This shift proved that"

# ----------------- UI LAYOUT -----------------

# 1. Main Header
st.markdown("""
<div class="header-container">
    <div class="gradient-title">🔮 AetherStory AI</div>
    <div class="header-subtitle">
        Generate premium, custom short stories instantly using Hugging Face's <b>gpt2</b> text-generation pipeline.
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Sidebar Parameters
with st.sidebar:
    st.markdown("## Configuration Engine")
    
    st.info("💡 **Model**: GPT-2 (Causal LM)\nLoaded via Transformers text-generation pipeline.")
    
    st.markdown("### Expected Skills")
    
    # Skill 1: max_length
    max_length = st.slider(
        "Max Length (Tokens)", 
        min_value=30, 
        max_value=300, 
        value=120, 
        step=10,
        help="The maximum number of tokens to generate. Includes prompt length."
    )
    
    # Skill 2: temperature
    temperature = st.slider(
        "Temperature", 
        min_value=0.1, 
        max_value=1.5, 
        value=0.8, 
        step=0.05,
        help="Higher values make output more random, creative, or chaotic. Lower values make it more deterministic."
    )
    
    # Skill 3: num_return_sequences
    num_return_sequences = st.slider(
        "Number of Sequences", 
        min_value=1, 
        max_value=3, 
        value=1, 
        step=1,
        help="Number of independent story variations to generate simultaneously."
    )
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #6b7280; font-size: 0.8rem;'>Powered by Hugging Face & Streamlit</div>", unsafe_allow_html=True)

# 3. Main Workspace - Preset Selectors
st.markdown("### 🪐 Select a Genre Preset")
col_space, col_horror, col_motiv = st.columns(3)

with col_space:
    if st.button("🌌 Space Story", use_container_width=True):
        apply_preset("space")
with col_horror:
    if st.button("🧟 Horror Story", use_container_width=True):
        apply_preset("horror")
with col_motiv:
    if st.button("✨ Motivational Paragraph", use_container_width=True):
        apply_preset("motivational")

st.markdown("<br>", unsafe_allow_html=True)

# 4. Prompt Input Text Area
prompt = st.text_area(
    "Edit or Write Your Prompt:", 
    key="prompt_input", 
    height=120,
    help="Start with your own idea or modify the preset text."
)

# 5. Generate Button
st.markdown("<br>", unsafe_allow_html=True)
generate_btn = st.button("🪄 Generate Story Chronicles", use_container_width=True)

# Loading the model pipeline
with st.spinner("Initializing GPT-2 text-generation pipeline... (this may take a few seconds on first run)"):
    generator = get_generator()

# 6. Inference Trigger
if generate_btn:
    if not prompt.strip():
        st.warning("Please enter a prompt to begin generation!")
    elif generator is None:
        st.error("Failed to generate stories because the text-generation pipeline is not loaded.")
    else:
        st.markdown("### 📜 Generated Chronicles")
        
        # Placeholder for animations
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            time.sleep(0.005)
            progress_bar.progress(i + 1)
            status_text.text(f"Analyzing prompt & generating continuation... {i+1}%")
            
        progress_bar.empty()
        status_text.empty()
        
        try:
            with st.spinner("Weaving the story threads together..."):
                stories = generate_stories(
                    generator=generator,
                    prompt=prompt,
                    max_length=max_length,
                    temperature=temperature,
                    num_return_sequences=num_return_sequences
                )
                
            # If multiple sequences, we display them side by side or as card grids
            if num_return_sequences > 1:
                cols = st.columns(num_return_sequences)
                for idx, story in enumerate(stories):
                    with cols[idx]:
                        # Format the output highlighting the prompt and the continuation
                        # Try to find prompt in the story to isolate the generated part
                        prompt_len = len(prompt)
                        generated_part = story[prompt_len:] if story.startswith(prompt) else story
                        
                        st.markdown(f"""
                        <div class="story-card">
                            <div class="story-header">
                                <span>Sequence {idx+1}</span>
                                <span class="tag-badge">Temp: {temperature}</span>
                            </div>
                            <span class="story-prompt-highlight">{prompt}</span>
                            <span class="story-body">{generated_part}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"💾 Download Sequence {idx+1}",
                            data=story,
                            file_name=f"story_sequence_{idx+1}.txt",
                            mime="text/plain",
                            key=f"dl_{idx}"
                        )
            else:
                story = stories[0]
                prompt_len = len(prompt)
                generated_part = story[prompt_len:] if story.startswith(prompt) else story
                
                st.markdown(f"""
                <div class="story-card">
                    <div class="story-header">
                        <span>Chronicle Output</span>
                        <span class="tag-badge">Temp: {temperature}</span>
                    </div>
                    <span class="story-prompt-highlight">{prompt}</span>
                    <span class="story-body">{generated_part}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.download_button(
                    label="💾 Download Story",
                    data=story,
                    file_name="story_chronicle.txt",
                    mime="text/plain",
                    key="dl_single"
                )
                
        except Exception as e:
            st.error(f"Error during story generation: {e}")
            st.info("Try reducing the Max Length or Number of Sequences parameters if the model encounters memory limits.")
