let expOrder = (function(i){
  if (i == 0){
    return ["modules/graphQuestions", "modules/debrief"]
  } else {
    return ["modules/graphInteract", "modules/debrief"]
  }
})
