import gradio as gr
import random
import time
from app.legal_document_utils import summarize, question_answer
from app.qdrant_cohere_utils import cross_lingual_document_search, translate_output
from app.examples import (
    GPL_LICENSE_DOC,
    GPL_LICENSE_QUESTION,
    POKEMON_GO_TERMS_OF_SERVICE,
    POKEMON_GO_QUESTION,
)

max_search_results = 3

def reset_chatbot():
    return gr.update(value="")


def user(input_question, history):
    return "", history + [[input_question, None]]


def legal_doc_qa_bot(input_document, history):
    bot_message = question_answer(input_document, history)
    history[-1][1] = bot_message
    # time.sleep(1)
    return history


with gr.Blocks() as demo:
    gr.HTML(
        """<html><center><img src='file/logo/flc_design4.png', alt='Legal-ease logo', width=250, height=250 /></center><br></html>"""
    )

    qa_bot_state = gr.State(value=[])

    with gr.Tabs():
        with gr.TabItem("Q&A"):
            gr.HTML("""<p style="text-align: center; font-weight: bold; color: maroon; font-size: 15px;">Legal Document Q&A</p>""")
            gr.HTML("""<p style="text-align:center;">We know legal documents can be dense to comprehend and difficult to understand. Add your legal document below and we'll answer all your doubts and queries.</p>""")
            
            with gr.Row():
                with gr.Column():
                    input_document = gr.Text(label="Copy your document here", lines=10)

                with gr.Column():
                    chatbot = gr.Chatbot(label="Chat History")
                    input_question = gr.Text(label="Ask a question")
                    clear = gr.Button("Clear")

            with gr.Row():
                with gr.Accordion("Show example inputs I can load:", open=False):
                    # example_1 = gr.Button("Load GPL License Document")
                    gr.Examples(
                        [
                            [GPL_LICENSE_DOC, GPL_LICENSE_QUESTION],
                            [POKEMON_GO_TERMS_OF_SERVICE, POKEMON_GO_QUESTION],
                        ],
                        [input_document, input_question],
                        [],
                        None,
                        cache_examples=False,
                    )

        with gr.TabItem("Summarize"):
            gr.HTML("""<p style="text-align: center; font-weight: bold; color: maroon; font-size: 15px;">Legal Document Summarization</p>""")
            gr.HTML("""<p style="text-align:center;">Legal documents can be way too lengthy and sometimes all you want is a quick high-level summary. Enter your legal document below and we'll summarize it for you.</p>""")
            
            with gr.Row():
                with gr.Column():
                    summary_input = gr.Text(label="Document", lines=10)
                    generate_summary = gr.Button("Generate Summary")

                with gr.Column():
                    summary_output = gr.Text(label="Summary", lines=10)

            with gr.Row():
                with gr.Accordion("Advanced Settings:", open=False):
                    
                    summary_length = gr.Radio(
                        ["short", "medium", "long"], label="Summary Length", value="long"
                    )
                    summary_format = gr.Radio(
                        ["paragraph", "bullets"], label="Summary Format", value="bullets"
                    )
                    extractiveness = gr.Radio(
                        ["low", "medium", "high"],
                        label="Extractiveness",
                        info="Controls how close to the original text the summary is.",
                        visible=False,
                        value="high",
                    )
                    temperature = gr.Slider(
                        minimum=0,
                        maximum=5.0,
                        value=0.64,
                        step=0.1,
                        interactive=True,
                        visible=False,
                        label="Temperature",
                        info="Controls the randomness of the output. Lower values tend to generate more “predictable” output, while higher values tend to generate more “creative” output.",
                    )
            with gr.Row():
                with gr.Accordion("Show example inputs I can load:", open=False):
                    gr.Examples(
                        [
                            [GPL_LICENSE_DOC],
                            [POKEMON_GO_TERMS_OF_SERVICE],
                        ],
                        [summary_input],
                        [],
                        None,
                        cache_examples=False,
                    )
                    
        with gr.TabItem("Document Search"):
            gr.HTML("""<p style="text-align: center; font-weight: bold; color: maroon; font-size: 15px;">Legal Document Search</p>""")
            gr.HTML("""<p style="text-align:center;">Search across a set of legal documents in any language or even a mix of languages. Query them using any one of over 100 supported languages.</p>""")
            
            gr.HTML("""<p style="text-align:center; font-style:italic;">To get you started, we have indexed a set of documents from eight European countries (Belgium, France, Hungary, Italy, Netherlands, Norway, Poland, UK) in seven languages, outlining legislation passed during the COVID-19 pandemic.</p>""")
            
#             gr.Markdown("""Search across a set of legal documents in any language or even a mix of languages. Query them using any one of over 100 supported languages.
# To get you started, we have indexed a set of documents from eight European countries (Belgium, France, Hunary, Italy, Netherlands, Norway, Poland, UK) in seven languages, outlining legislation passed during the COVID-19 pandemic.""")
            
            with gr.Row():
                text_match = gr.CheckboxGroup(["Full Text Search"], label="find exact text in documents")
                doc_choices = gr.CheckboxGroup(["contracts", "legislations", "caselaw", "terms of service"], label="Search through these documents", visible=False)
            with gr.Row():
                lang_choices = gr.CheckboxGroup(["English", "French", "Italian", "Dutch", "Polish", "Hungarian", "Norwegian"], label="Filter results based on language")                
                
            with gr.Row():
                with gr.Column():
                    user_query = gr.Text(label="Enter query here", placeholder="Search through all your documents")
                    
                    num_search_results = gr.Slider(1, max_search_results, visible=False, value=max_search_results, step=1, interactive=True, label="How many search results to show:")
                                       
                    with gr.Row():
                        with gr.Column():
                            query_match_out_1 = gr.Textbox(label=f"Search Result 1")
                        
                        with gr.Column():
                            with gr.Accordion("Translate Search Result", open=False):
                                translate_1 = gr.Button(label="Translate", value="Translate")
                                translate_res_1 = gr.Textbox(label=f"Translation Result 1")
                                
                    with gr.Row():
                        with gr.Column():
                            query_match_out_2 = gr.Textbox(label=f"Search Result 2")

                        with gr.Column():
                            with gr.Accordion("Translate Search Result", open=False):
                                translate_2 = gr.Button(label="Translate", value="Translate")
                                translate_res_2 = gr.Textbox(label=f"Translation Result 2")
                                
                    with gr.Row():        
                        with gr.Column():
                            query_match_out_3 = gr.Textbox(label=f"Search Result 3")

                        with gr.Column():
                            with gr.Accordion("Translate Search Result", open=False):
                                translate_3 = gr.Button(label="Translate", value="Translate")
                                translate_res_3 = gr.Textbox(label=f"Translation Result 3")
                
    
    # fetch answer for submitted question corresponding to input document
    input_question.submit(
        user, [input_question, chatbot], [input_question, chatbot], queue=False
    ).then(legal_doc_qa_bot, [input_document, chatbot], chatbot)

    # reset the chatbot Q&A history when input document changes
    input_document.change(fn=reset_chatbot, inputs=[], outputs=chatbot)
    
    # generate summary corresponding to document submitted by the user.
    generate_summary.click(
        summarize,
        [summary_input, summary_length, summary_format, extractiveness, temperature],
        [summary_output],
        queue=False,
    )

    # clear the chatbot Q&A history when this button is clicked by the user
    clear.click(lambda: None, None, chatbot, queue=False)
    
    # run search as user is typing the query
    user_query.change(cross_lingual_document_search, [user_query, num_search_results, lang_choices, doc_choices, text_match], [query_match_out_1, query_match_out_2, query_match_out_3], queue=False)
    
    # run search if user submits query
    user_query.submit(cross_lingual_document_search, [user_query, num_search_results, lang_choices, doc_choices, text_match], [query_match_out_1, query_match_out_2, query_match_out_3], queue=False)
    
    
    # translate results corresponding to 1st search result obtained if user clicks 'Translate'
    translate_1.click(
        translate_output,
        [query_match_out_1, user_query],
        [translate_res_1],
        queue=False,
    )
    
    # translate results corresponding to 2nd search result obtained if user clicks 'Translate'
    translate_2.click(
        translate_output,
        [query_match_out_2, user_query],
        [translate_res_2],
        queue=False,
    )
    
    # translate results corresponding to 3rd search result obtained if user clicks 'Translate'
    translate_3.click(
        translate_output,
        [query_match_out_3, user_query],
        [translate_res_3],
        queue=False,
    )


if __name__ == "__main__":
    demo.launch(debug=True)
