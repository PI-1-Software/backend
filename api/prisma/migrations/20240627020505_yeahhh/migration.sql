-- CreateTable
CREATE TABLE "Carrinho" (
    "id" SERIAL NOT NULL,
    "consumo_energetico" DOUBLE PRECISION NOT NULL,
    "motor" TEXT NOT NULL,
    "velocidade_media" DOUBLE PRECISION NOT NULL,
    "aceleracao" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "Carrinho_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Trajeto" (
    "id" SERIAL NOT NULL,
    "distancia" DOUBLE PRECISION,
    "inicio" TIMESTAMP(3) NOT NULL,
    "fim" TIMESTAMP(3),
    "tempo" DOUBLE PRECISION,
    "velocidade_media" DOUBLE PRECISION,
    "aceleracao" DOUBLE PRECISION,
    "consumo_energetico" DOUBLE PRECISION,
    "carrinho_id" INTEGER NOT NULL,

    CONSTRAINT "Trajeto_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Registro" (
    "id" SERIAL NOT NULL,
    "id_trajeto" INTEGER NOT NULL,
    "velocidade_instantanea" DOUBLE PRECISION NOT NULL,
    "aceleracao_instantanea" DOUBLE PRECISION NOT NULL,
    "consumo_energetico" DOUBLE PRECISION NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Registro_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Trajeto" ADD CONSTRAINT "Trajeto_carrinho_id_fkey" FOREIGN KEY ("carrinho_id") REFERENCES "Carrinho"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Registro" ADD CONSTRAINT "Registro_id_trajeto_fkey" FOREIGN KEY ("id_trajeto") REFERENCES "Trajeto"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
