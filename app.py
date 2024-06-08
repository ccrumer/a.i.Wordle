import streamlit as st
from images import get_image, fetch_image_urls, fetch_random_image_url
from comparison import compare_images, guess_quality

#session state
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

if 'game_over' not in st.session_state:
    st.session_state.game_over = False

if 'guesses' not in st.session_state:
    st.session_state.guesses = []

if 'reference_image_url' not in st.session_state:
    st.session_state.reference_image_url = fetch_random_image_url()

st.set_page_config(page_title="NERD-LE")

#app css
st.markdown("""
    <style>
       
        .stApp {
            
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        /* Title */
        .title {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            font-family: 'Arial', sans-serif;
            color: #007BFF;
            margin-bottom: 10px;
        }
        /* Reference Image */
        .reference-image img {
            max-width: 100%;
            height: auto;
        }
        .attempts {
            text-align: center;
            margin: 20px 0;
        }
        .reference-image, .user-image {
            display: flex;
            justify-content: center;
        }
        .excellent-guess {
            color: purple;
        }
        .good-guess {
        
            color:green
        }
        .fair-guess {
            color: orange;
        }
        .bad-guess {
            color: red;
        }
        .guess-box {
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("<div class='title'>NERD-LE</div>", unsafe_allow_html=True)

# Display reference image
st.image(st.session_state.reference_image_url, use_column_width=True)

# Form to input the prompt
with st.form("prompt_form"):
    prompt1 = st.text_input("Guess the prompt used to create this image:", key="prompt1")
    submitted = st.form_submit_button("Generate Image")

if st.session_state.game_over:
    st.sidebar.write("Game Over! You've used all your attempts.")
else:
    if submitted and prompt1:
        with st.spinner("Generating your image..."):
            image1_url = get_image(prompt1)
            st.session_state.image1_url = image1_url
            st.session_state.attempts += 1

            if st.session_state.image1_url:
                similarity_score = compare_images(st.session_state.image1_url, st.session_state.reference_image_url)
                quality = guess_quality(similarity_score)
                st.session_state.guesses.append({
                    'image_url': st.session_state.image1_url,
                    'similarity_score': similarity_score,
                    'quality': quality
                })

            if st.session_state.attempts >= 3:
                st.session_state.game_over = True
                st.sidebar.write("Game Over! You've used all your attempts.")
                if guess_quality(similarity_score) == "Excellent Guess":
                    st.balloons()
            else:
                st.sidebar.write(f"Attempts left: {3 - st.session_state.attempts}")

# Display the guesses
st.sidebar.subheader("Your Guesses")
columns = st.sidebar.columns(3)

for idx, guess in enumerate(st.session_state.guesses):
    quality_class = guess['quality'].replace(' ', '-').lower()
    with columns[idx % 3]:
        st.markdown(f"<div class='guess-box {quality_class}'>", unsafe_allow_html=True)
        st.image(guess['image_url'], caption=f"Score: {guess['similarity_score']*100:.2f}%", use_column_width=True)
        st.markdown(f"<div class='{quality_class}' style='text-align: center;'>{guess['quality']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# play again
if st.session_state.game_over:
    if st.sidebar.button("Play Again"):
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.guesses = []
        st.session_state.reference_image_url = fetch_random_image_url()
        st.experimental_rerun()

