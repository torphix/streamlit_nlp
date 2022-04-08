import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Calendar from "rc-year-calendar"
import { Map } from "typescript"

interface State {
  calendarName: string
  dataSource: any[]
}

const currentYear = new Date().getFullYear()


/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class CalendarComponent extends StreamlitComponentBase<State> {
  public state = {
    calendarName: "",
    dataSource: [
      { id: 0, name: "Entry 1", startDate: new Date(currentYear, 4, 28) },
    ],
  }

  public render = (): ReactNode => {
    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.
    const { theme } = this.props
    const style: React.CSSProperties = {}

    return (
      <Calendar
        displayHeader={this.state.calendarName}
        dataSource={this.state.dataSource}
      />
    )
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(CalendarComponent)
