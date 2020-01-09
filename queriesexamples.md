mutation createList {
  createList(input: {
    name: "Plan to The Future"
  }) {
    ok
  }
  
}

{
  lists {
    name
    id,
    tasks {
      text
    }
  }
}

{
  list(id: 1) {
    tasks {
      id
      text
    }
  }
}

mutation updateList {
  updateList(id: 3, input: {
    name: "What I did"
  }) {
    ok
  }
}

#---------------------

mutation createTask {
  createTask(input: {
    text: "Learn not to be an asshole",
    list: 1
  }) {
    ok
  }
}

{
  task(id: 3) {
    text
  }
}

{
	tasks {
    text
  }
}

mutation updateTask {
  updateTask(id: 3, input:{
    text: "To be AWES"
  }) {
    ok
  }
}