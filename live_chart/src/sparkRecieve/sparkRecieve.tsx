import { useEffect, useState } from "react";
// import LineChart from "../chart/resultTradingChart";

interface Data {
    closes: number;
    buys?: number | null;
    sells?: number | null;
  }
  
  interface Props {
    data: Data[];
  }

const WebSocketComponent = () => {
  const [data, setData] = useState<Props>({ data: [] });
  console.log(data)

  useEffect(() => {
    const client = new WebSocket("ws://localhost:8765");

    client.onmessage = (message) => {
        const receivedData: string = message.data;
        try {
          const parsedData: Props = JSON.parse(receivedData);
          setData((prevData) => ({ data: prevData.data.concat(parsedData.data) }));
        } catch (error) {
          console.error("Error parsing JSON data:", error);
        }
      };
      
  }, []);

  return (
    <div>
      {/* <LineChart data={data.data} /> */}
    </div>
  );
};

export default WebSocketComponent;
