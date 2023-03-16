import gradio as gr
import random
import time
from legal_document_utils import summarize, question_answer
from examples import (
    GNU_LICENSE_DOC,
    GNU_LICENSE_QUESTION,
    POKEMON_GO_TERMS_OF_SERVICE,
    POKEMON_GO_QUESTION,
)


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
        """<html><center><img src='file/flc_design4.png', alt='Legal-ease logo', width=150, height=150 /></center><br></html>"""
    )

    qa_bot_state = gr.State(value=[])

    with gr.Tabs():
        with gr.TabItem("Q&A"):
            with gr.Row():
                with gr.Column():
                    input_document = gr.Text(label="Copy your document here", lines=10)

                with gr.Column():
                    chatbot = gr.Chatbot()
                    input_question = gr.Text(label="Ask a question")
                    clear = gr.Button("Clear")

            with gr.Row():
                with gr.Accordion("Show example inputs I can load:", open=False):
                    gr.Examples(
                        [
                            [GNU_LICENSE_DOC, GNU_LICENSE_QUESTION],
                            [POKEMON_GO_TERMS_OF_SERVICE, POKEMON_GO_QUESTION],
                        ],
                        [input_document, input_question],
                        [],
                        None,
                        cache_examples=False,
                    )

        with gr.TabItem("Summarize"):
            with gr.Row():
                with gr.Column():
                    summary_input = gr.Text(label="Document", lines=10)
                    generate_summary = gr.Button("Generate Summary")

                with gr.Column():
                    summary_output = gr.Text(label="Summary", lines=10)

            with gr.Row():
                with gr.Accordion("Advanced Settings:", open=False):
                    # model = # summarize-xlarge or summarize-medium
                    summary_length = gr.Radio(
                        ["short", "medium", "long"], label="Summary Length"
                    )
                    summary_format = gr.Radio(
                        ["paragraph", "bullet"], label="Summary Format"
                    )
                    extractiveness = gr.Radio(
                        ["low", "medium", "high"],
                        label="Extractiveness",
                        info="Controls how close to the original text the summary is.",
                    )
                    temperature = gr.Slider(
                        minimum=0,
                        maximum=5.0,
                        value=0.64,
                        step=0.1,
                        interactive=True,
                        label="Temperature",
                        info="Controls the randomness of the output. Lower values tend to generate more “predictable” output, while higher values tend to generate more “creative” output.",
                    )

    input_question.submit(
        user, [input_question, chatbot], [input_question, chatbot], queue=False
    ).then(legal_doc_qa_bot, [input_document, chatbot], chatbot)

    # reset the chatbot Q&A history when input document changes
    input_document.change(fn=reset_chatbot, inputs=[], outputs=chatbot)

    # clear the chatbot Q&A history when this button is clicked by the user
    clear.click(lambda: None, None, chatbot, queue=False)

    generate_summary.click(
        summarize,
        [summary_input, summary_length, summary_format, extractiveness, temperature],
        [summary_output],
        queue=False,
    )


if __name__ == "__main__":
    demo.launch(debug=True)
