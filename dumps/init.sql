CREATE DATABASE  IF NOT EXISTS `datapath` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `datapath`;
-- MySQL dump 10.13  Distrib 8.0.36, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: datapath
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `uuid_cliente` varchar(50) NOT NULL,
  `nombre_cliente` varchar(255) DEFAULT NULL,
  `edad` int DEFAULT NULL,
  `genero` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`,`uuid_cliente`),
  UNIQUE KEY `uuid_cliente` (`uuid_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=14753 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `fecha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fecha` (
  `id_fecha` int NOT NULL AUTO_INCREMENT,
  `uuid_fecha` varchar(50) NOT NULL,
  `fec_pedido` date DEFAULT NULL,
  `fec_prime` date DEFAULT NULL,
  `fec_vto` date DEFAULT NULL,
  `fec_mora` date DEFAULT NULL,
  `anio` int DEFAULT NULL,
  `mes` int DEFAULT NULL,
  `dia` int DEFAULT NULL,
  `mes_nombre` varchar(50) DEFAULT NULL,
  `trimestre` smallint DEFAULT NULL,
  `semestre` smallint DEFAULT NULL,
  PRIMARY KEY (`id_fecha`,`uuid_fecha`),
  UNIQUE KEY `uuid_fecha` (`uuid_fecha`)
) ENGINE=InnoDB AUTO_INCREMENT=14753 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id_pedido` int NOT NULL AUTO_INCREMENT,
  `uuid_pedido` varchar(50) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `categoria` varchar(255) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `descuento` float DEFAULT NULL,
  PRIMARY KEY (`id_pedido`,`uuid_pedido`),
  UNIQUE KEY `uuid_pedido` (`uuid_pedido`)
) ENGINE=InnoDB AUTO_INCREMENT=14753 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `uuid_producto` varchar(50) NOT NULL,
  `nombre_producto` varchar(255) DEFAULT NULL,
  `precio` float DEFAULT NULL,
  `igv` float DEFAULT NULL,
  PRIMARY KEY (`id_producto`,`uuid_producto`),
  UNIQUE KEY `uuid_producto` (`uuid_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=14753 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `sistema_ventas`
--

DROP TABLE IF EXISTS `sistema_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sistema_ventas` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `cliente_id_cliente` varchar(50) NOT NULL,
  `pedido_id_pedido` varchar(50) NOT NULL,
  `fecha_id_fecha` varchar(50) NOT NULL,
  `producto_id_producto` varchar(50) NOT NULL,
  PRIMARY KEY (`id_venta`),
  KEY `cliente_id_cliente` (`cliente_id_cliente`),
  KEY `pedido_id_pedido` (`pedido_id_pedido`),
  KEY `fecha_id_fecha` (`fecha_id_fecha`),
  KEY `producto_id_producto` (`producto_id_producto`),
  CONSTRAINT `sistema_ventas_ibfk_1` FOREIGN KEY (`cliente_id_cliente`) REFERENCES `cliente` (`uuid_cliente`),
  CONSTRAINT `sistema_ventas_ibfk_2` FOREIGN KEY (`pedido_id_pedido`) REFERENCES `pedido` (`uuid_pedido`),
  CONSTRAINT `sistema_ventas_ibfk_3` FOREIGN KEY (`fecha_id_fecha`) REFERENCES `fecha` (`uuid_fecha`),
  CONSTRAINT `sistema_ventas_ibfk_4` FOREIGN KEY (`producto_id_producto`) REFERENCES `producto` (`uuid_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=14753 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
