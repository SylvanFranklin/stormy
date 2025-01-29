#set page(flipped: true, background: image("ship_red.jpeg"))

#table(columns: 9)
#circle(width: 1in, height: 1in)


#place(center + bottom)[
  #for i in range(10) {
    box(width: 0.75in, height: 0.75in, stroke: 0.22em, fill: white)[#place(center + horizon)[#text(16pt)[#i]]]
  }
]


