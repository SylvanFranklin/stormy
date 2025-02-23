

For each unwilling helen check the nearest city, and consult the chart based on if they have a Helen

#table(columns: 3)[No Helen][Willing Helen][Unwilling Helen][Place the helen here][Run further][This Helen takes the place of the existing Helen, that helen runs further]

Running Further: Use the swept to location on leading players card. All Helens running further will jump to the closest palace in the next region in the direction of the swept to location. If a running further helen is already in the swept to region she will attempt to jump to the next closest palace in that region. Use the above table to determine what happens when a helen reaches a new palace, it may result in multiple jumps.

When an unwilling finds a home it becomes willing. 

#import "@preview/fletcher:0.5.4" as fletcher: diagram, node, edge
#import fletcher.shapes: hexagon

#diagram(
	node-stroke: .1em,
	spacing: 4em,
	edge((-1,0), "r", "-|>", [Unwilling Helen], label-pos: 0, label-side: left),
	node((0,0), [Closest Palace \ in region], radius: 4em),
	edge((0, 0), (2, 0), `has willing`, "-|>", label-angle: auto, bend: 30deg),
	edge((0,0), (1.3,.7), `has unwilling`, "-|>", label-angle: auto),
	node((1.3,.7), [Take place of this Helen], radius: 3em),
	node((2, 0), [Move over one region \ in the direction of swept to]),
	edge((1.3,.7), (2, 0), `new Helen`, "--|>", bend: -10deg, label-angle: auto),
	edge((0,0), (0,0), `no Helen`, "--|>", bend: 130deg),
	edge((2,0), (0,0), `Start Over`, "--|>"),
)
