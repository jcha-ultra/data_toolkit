# Creates a barebones Shiny app on a local server.

library(shiny)

get_output <- function(input) {
  paste0("Your text was: '", input, "'")
}

# creates a local server
server <- function(input, output) {
  # sets the print value of the output
  output$value <- shiny::renderPrint({
    # processes the input; this is the input value that was ingested from the user in the ui object below
    get_output(input$text)
  })
}

# creates a page for users; the inputs to `fluidPage` are the elements of the page
ui <- fluidPage(
  # text input; notice that the "text" `inputId` is referenced again in the server via `input$text`
  textAreaInput(inputId = "text", label = "add some text here", rows = 6),
  # break line
  hr(),
  # prints the output that was created in the `server` function
  fluidRow(column(3, verbatimTextOutput("value")))
)

shinyApp(ui, server)
