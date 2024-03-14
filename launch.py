if __name__ == "__main__":
  import gradio as gr
  import importlib
  
  def single_infer(multi:bool=False):
    import json, random
    with open("items.json", "r", encoding="utf-8") as f:
      ids = json.load(f)["d"]
    
    if multi: return ids
    return random.choice(ids), "Success."


  def multi_infer(chance:(float | int)=0.01, adv_compability=False):
    chance *= 100
    
    import random
    dates = single_infer(True)
    random.shuffle(dates)
    
    data = [x for x in dates if random.randrange(1, 10000, step=1) <= chance]
    if adv_compability:
      return data
    
    text = ""
    for x in data:
      text += str(x)+", "
    
    return text.strip(", "), "Success."
  

  def get_data_count() -> int:
    import os, json
    if os.path.exists("items.json"):
      with open("items.json", "r", encoding="utf-8") as f:
        return len(json.load(f)["d"])
      
    else:
      return 0
  
  
  def get_data_count_formatted():
    return f"{get_data_count()} items registered"
  
  
  def refresh_id(mcver):
    import os
    if os.path.exists("./obtain_item.py"):
      module = importlib.import_module("obtain_item")
      
      func = module.__dict__["obtain_item"]
      if callable(func):
        func(mcver)
        return "Success. Restart ui will update the count range in \"Adv. Multiple mode\""#, gr.Slider.update(max=get_data_count())
      else:
        return f"Failed. {func} is not callable"#, gr.Slider.update(visible=True)
    else:
      return "Failed. files not found."#, gr.Slider.update(visible=True)
  
  def adv_infer(chance, count):
    import random
    data:list = multi_infer(100, True)
    
    while len(data) != count:
      if (random.randrange(1, 10000)/100) <= (chance * 33):
        data.remove(data[random.randrange(0, (len(data)))])

    text = ""
    for x in data:
      text += x+", "
    return text.strip(", "), "Success."
  
    
  ui = gr.Blocks(title="mcitem_randselector")
  with ui:
    item_count = gr.Markdown(get_data_count_formatted, every=1.0)
    
    mcver = gr.Radio(choices=["1.12.2", "1.16.5"], label="Minecraft Version", value="1.16.5")
    refresh_ids = gr.Button("Change Target MCVer")
    gr.Markdown("<br />")
    

    with gr.Blocks():
      res = gr.Textbox(label="result")
      
      with gr.Row():
        get_btn = gr.Button("Choose Item")
        
        with gr.Accordion(label="Multiple mode",open=False):
          multi_chance = gr.Slider(0.01, 100, value=0.75, step=0.01, label="Chosen Chance")
          multi_btn = gr.Button("Choose Items")

        with gr.Accordion(label="Adv. Multiple mode", open=False):
          multi_count = gr.Slider(1, get_data_count(), value=int(get_data_count()/120), label="count", step=1)
          multi_chance2 = gr.Slider(0.01, 100, value=0.75, step=0.01, label="Chosen Chance")
          adv_btn = gr.Button("Choose Items")
    
    status = gr.Textbox(label="status")
  
    refresh_ids.click(
      refresh_id, mcver, outputs=[status]
    )
    get_btn.click(
     single_infer, outputs=[res, status] 
    )
    multi_btn.click(
      multi_infer, multi_chance, [res, status] 
    )
    adv_btn.click(
      adv_infer, [multi_chance2, multi_count], [res, status]
    )
  
  ui.queue(64)
  ui.launch()
  