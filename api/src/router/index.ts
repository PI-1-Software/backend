import { Express } from "express";
import prismaClient from "../db/Prisma";

let current_trajeto: number;

export function setupRoutes(app: Express) {
  app.post("/receba", async (req, res) => {
    const data = req.body as Array<{
      x: number;
      y: number;
      aceleracao: number;
      velocidade: number;
      consumo_energetico: number;
      distancia: number;
      tempo: number;
    }>;

    const isBegin = data[0].x === 0 && data[0].y === 0;
    if (isBegin) {
      const trajeto = await prismaClient.trajeto.create({
        data: {
          carrinho_id: 1, // TODO: set the correct value
          inicio: new Date(),
        },
      });
      current_trajeto = trajeto.id;
    }

    for (const obj of data) {
      // TODO: add missing treatment of data
      await prismaClient.registro.create({
        data: {
          id_trajeto: current_trajeto,
          aceleracao_instantanea: obj.aceleracao,
          velocidade_instantanea: obj.velocidade,
          consumo_energetico: obj.consumo_energetico,
        },
      });
    }

    return res.send({
      response: "ok",
    });
  });

  app.post("/carrinho", async (req, res) => {
    const data = req.body as {
      aceleracao: number;
      motor: string;
      velocidade_media: number;
      consumo_energetico: number;
    };

    await prismaClient.carrinho.create({
      data,
    });

    return res.send({
      response: "ok",
    });
  });
}
