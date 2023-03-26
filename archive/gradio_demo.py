import gradio as gr
from legal_document_utils import summarize, question_answer

qa_demo = gr.Interface( 
              title = "<html><center><img src='file/flc_design4.png', alt='Legal-ease logo', width=300, height=300 /></center><br></html> For all your legalese ...",
              description="<html><center>Copy-paste the contents of your document, and post your question about it. It's that easy!</center></html>",
              fn=question_answer, 
              inputs=[
                     gr.Text(label= "Copy your document here", lines=20), 
                     gr.Text(label= "Ask a question")
                    ], 
              outputs=[
                        gr.Text(label='Answer')
                        ]
            )

summarize_demo = gr.Interface(
                    title = "<html><center><img src='file/flc_design4.png', alt='Legal-ease logo', width=300, height=300 /></center><br></html> For all your legalese ...",
                    description="<html><center>Copy-paste the contents of your document and get a neat summary with just a click!</html>",
                    fn=summarize,
                    inputs=[gr.Text(label='Document', lines=30)],
                    outputs=[gr.Text(label = "Summary", lines=30)]
                )

gr.TabbedInterface(
    [qa_demo, summarize_demo], ["QA", "Summarize"]
).launch()