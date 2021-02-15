from graphviz import render, Source

src = Source.from_file("./test.gv", engine="neato")

src.render()