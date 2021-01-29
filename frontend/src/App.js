import React, { useEffect, useState } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Card } from "react-bootstrap";

function App() {
  const [isloading, setIsloading] = useState(false);
  const [message, setMessage] = useState([]);
  //const api_url = process.env.API_URL

  const getmessage = () => {
    const apiUrl = "http://localhost:5000/stats";
    fetch(apiUrl)
      .then((res) => res.json())
      .then((message) => {
        setIsloading(true);
        setMessage(message);
      })
      .catch((e) => {
        console.log(e);
      });
  };
  useEffect(() => {
    getmessage();
    const interval = setInterval(() => {
      getmessage();
    }, 1000);
    return () => clearInterval(interval);
  }, []);
  return (
    <div className="App">
      <Card style={{ width: "18rem" }} bg="success" border="none">
        <Card.Header>Average Time</Card.Header>
        <Card.Body>
          <Card.Text>{(message.average_time * 1000).toFixed(2)} ms</Card.Text>
        </Card.Body>
      </Card>

      <br />

      <Card style={{ width: "18rem" }} bg="info">
        <Card.Header>Total Messages</Card.Header>
        <Card.Body>
          <Card.Text>{message.max_message_number}</Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
}

export default App;
