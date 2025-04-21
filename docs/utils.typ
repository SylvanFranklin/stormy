#let icon(path) = {
  box(baseline: 20%, width: 1.3em, height: 1.3em)[#image(path)]
}
#let recipe(arr) = {
  for elm in arr {
    elm
  }
}

#let light = icon("light.svg")
#let heavy = icon("heavy.svg")
#let medium = icon("medium.svg")
#let wits = icon("wits.svg")
#let charm = icon("charm.svg")
#let might = icon("might.svg")

#let all = (light, medium, heavy, wits, charm, might)

#let orb = i => circle(fill: white, radius: 0.75in, stroke: 4pt)[#align(center + horizon)[#text(60pt)[#i]]]

