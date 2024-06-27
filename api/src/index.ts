import 'dotenv/config';
import cors from "cors";
import express from "express";
import { setupRoutes } from "./router";

const app = express();

app.use(express.json());
app.use(cors());

setupRoutes(app);

app.listen(3000, () => {
  console.log("Server is running on http://localhost:3000");
});
  