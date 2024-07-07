CREATE TABLE "records" (
    "id_path" INTEGER NOT NULL,
    "position" POINT NOT NULL,
    "instant_velocity" DOUBLE PRECISION NOT NULL,
    "instant_acceleration" DOUBLE PRECISION NOT NULL,
    "energy_consumption" DOUBLE PRECISION NOT NULL,
    "timestamp" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX "records_id_path" ON "records" ("id_path");
CREATE INDEX "records_timestamp" ON "records" ("timestamp");
