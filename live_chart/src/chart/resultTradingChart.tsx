// import React from "react";
// import { Line } from "react-chartjs-2";
// import { ChartData, ChartDataset } from "chart.js";

// interface Data {
//   closes: number;
//   buys?: number | null;
//   sells?: number | null;
// }

// interface Props {
//   data: Data[];
// }

// const LineChart: React.FC<Props> = ({ data }) => {
//   const chartData: ChartData<"line", ChartDataset<"line", number[]>[]> = {
//     labels: data.map((_, index) => (index + 1).toString()),
//     datasets: [
//       {
//         label: "Closes",
//         data: data.map((item) => item.closes),
//         borderColor: "blue",
//         fill: false,
//       },
//       {
//         label: "Buy",
//         data: data
//           .filter((item) => item.buys !== undefined && item.buys !== null)
//           .map((item, index) => ({
//             x: index + 1,
//             y: item.buys!,
//           })),
//         borderColor: "green",
//         fill: false,
//       },
//       {
//         label: "Sell",
//         data: data
//           .filter((item) => item.sells !== undefined && item.sells !== null)
//           .map((item, index) => ({
//             x: index + 1,
//             y: item.sells!,
//           })),
//         borderColor: "red",
//         fill: false,
//       },
//     ],
//   };

//   return <Line data={chartData} />;
// };

// export default LineChart;
