
import React from 'react';

export default class App extends React.Component {
  render() {
    return (
      <div className="tabsDynamicHeight">
        <div>
          <ul className="horizontalMenu">
            <li label="Round Trip">
              <h1 className="md-display-2">Round Trip</h1>
            </li>
            <li label="One Way">
              <h1 className="md-display-2">One Way</h1>
            </li>
            <li label="Multi-city">
              <h1 className="md-display-2">Multi-city</h1>
            </li>
          </ul>
        </div>

      <hr/>
      </div>);
  }
}
