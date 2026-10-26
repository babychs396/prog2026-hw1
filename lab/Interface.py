import gradio as gr
from analyzer import check_apostrophes, process_file

COLORS = {"виправлено": "#c084fc", "перевірте": "#facc15"}

with gr.Blocks() as demo:
    gr.Markdown("# Перевірка апострофа\n\nМодуль знаходить пропущені й зайві апострофи за правописом "
                "та сліди російської орфографії. "
                "Виправлення перевіряються за словником pymorphy3: фіолетовим позначено виправлені слова, "
                "жовтим – слова, які варто перевірити вручну, адже їх немає в словнику.")
    check_rus = gr.Checkbox(value=True, label="Шукати сліди російської орфографії")

    with gr.Tabs():
        with gr.TabItem("Ввести текст"):
            with gr.Row():
                with gr.Column(scale=1):
                    input_text = gr.Textbox(
                        label="Ваш текст українською",
                        lines=10,
                    )
                    analyze_text_btn = gr.Button("Перевірити текст", variant="primary")
                with gr.Column(scale=1):
                    output_text = gr.Textbox(label="Виправлений текст", lines=5,
                                             interactive=False, buttons=["copy"])
                    output_highlight = gr.HighlightedText(label="Що змінилося", color_map=COLORS,
                                                          show_legend=True)
                    output_stats = gr.Markdown()
                    with gr.Accordion("Виправлені помилки", open=False):
                        output_log = gr.Markdown()

            analyze_text_btn.click(
                fn=check_apostrophes,
                inputs=[input_text, check_rus],
                outputs=[output_text, output_highlight, output_stats, output_log]
            )

        with gr.TabItem("Завантажити файл"):
            with gr.Row():
                with gr.Column(scale=1):
                    input_file = gr.File(label="Завантажте .txt файл")
                    analyze_file_btn = gr.Button("Обробити файл", variant="primary")
                with gr.Column(scale=1):
                    output_text_file = gr.Textbox(label="Виправлений текст", lines=5,
                                                  interactive=False, buttons=["copy"])
                    output_highlight_file = gr.HighlightedText(label="Що змінилося", color_map=COLORS,
                                                               show_legend=True)
                    output_stats_file = gr.Markdown()
                    with gr.Accordion("Виправлені помилки", open=False):
                        output_log_file = gr.Markdown()

            analyze_file_btn.click(
                fn=process_file,
                inputs=[input_file, check_rus],
                outputs=[output_text_file, output_highlight_file, output_stats_file, output_log_file]
            )

    demo.launch(share=True, theme=gr.themes.Soft(primary_hue="violet", secondary_hue="purple"))
