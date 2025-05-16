-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         11.7.2-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para taller_pintura
CREATE DATABASE IF NOT EXISTS `taller_pintura` /*!40100 DEFAULT CHARACTER SET armscii8 COLLATE armscii8_bin */;
USE `taller_pintura`;

-- Volcando estructura para tabla taller_pintura.detalleventa
CREATE TABLE IF NOT EXISTS `detalleventa` (
  `idDetalleVenta` int(11) NOT NULL AUTO_INCREMENT,
  `idVenta` int(11) NOT NULL,
  `idServicio` int(11) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `Subtotal` decimal(10,2) NOT NULL,
  `Devolucion` tinyint(1) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idDetalleVenta`),
  KEY `IX_Relationship6` (`idVenta`),
  KEY `IX_Relationship1_DV` (`idServicio`),
  CONSTRAINT `FK_DetalleVenta_Servicio` FOREIGN KEY (`idServicio`) REFERENCES `servicio` (`idServicio`),
  CONSTRAINT `FK_DetalleVenta_Venta` FOREIGN KEY (`idVenta`) REFERENCES `venta` (`idVenta`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.devolucion
CREATE TABLE IF NOT EXISTS `devolucion` (
  `idDevolucion` int(11) NOT NULL AUTO_INCREMENT,
  `FechaDevolucion` date NOT NULL,
  `Motivo` varchar(200) NOT NULL,
  `idDetalleVenta` int(11) DEFAULT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idDevolucion`),
  KEY `IX_Relationship12` (`idDetalleVenta`),
  CONSTRAINT `FK_Devolucion_DetalleVenta` FOREIGN KEY (`idDetalleVenta`) REFERENCES `detalleventa` (`idDetalleVenta`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.inventario
CREATE TABLE IF NOT EXISTS `inventario` (
  `idInventario` int(11) NOT NULL AUTO_INCREMENT,
  `TipoInventario` int(11) NOT NULL,
  `NombreProducto` varchar(100) NOT NULL,
  `idTipoPintura` int(11) DEFAULT NULL,
  `Lote` varchar(50) DEFAULT NULL,
  `CodigoColor` varchar(100) DEFAULT NULL,
  `CantidadDisponible` int(11) NOT NULL,
  `FechaAdquisicion` date DEFAULT NULL,
  `FechaVencimiento` date DEFAULT NULL,
  `EstadoInventario` tinyint(1) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idInventario`),
  KEY `IX_Relationship5_Inv` (`idTipoPintura`),
  CONSTRAINT `FK_Inventario_TipoPintura` FOREIGN KEY (`idTipoPintura`) REFERENCES `tipopintura` (`idTipoPintura`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.movimiento
CREATE TABLE IF NOT EXISTS `movimiento` (
  `idMovimiento` int(11) NOT NULL AUTO_INCREMENT,
  `idInventario` int(11) DEFAULT NULL,
  `TipoMovimiento` varchar(100) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `FechaMovimiento` datetime NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idMovimiento`),
  KEY `IX_Relationship6_Mov` (`idInventario`),
  CONSTRAINT `FK_Movimiento_Inventario` FOREIGN KEY (`idInventario`) REFERENCES `inventario` (`idInventario`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.precioserviciovehiculo
CREATE TABLE IF NOT EXISTS `precioserviciovehiculo` (
  `idPrecioServicioVehiculo` int(11) NOT NULL AUTO_INCREMENT,
  `idTipoServicio` int(11) NOT NULL,
  `idTipoVehiculo` int(11) NOT NULL,
  `Precio` decimal(10,2) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idPrecioServicioVehiculo`),
  KEY `IX_Relationship2` (`idTipoServicio`),
  KEY `IX_Relationship3` (`idTipoVehiculo`),
  CONSTRAINT `FK_Precio_TipoServicio` FOREIGN KEY (`idTipoServicio`) REFERENCES `tiposervicio` (`idTipoServicio`),
  CONSTRAINT `FK_Precio_TipoVehiculo` FOREIGN KEY (`idTipoVehiculo`) REFERENCES `tipovehiculo` (`idTipoVehiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.servicio
CREATE TABLE IF NOT EXISTS `servicio` (
  `idServicio` int(11) NOT NULL AUTO_INCREMENT,
  `NombreServicio` varchar(100) NOT NULL,
  `DescripcionServicio` varchar(150) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `ValidoDev` tinyint(1) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idServicio`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.tipopintura
CREATE TABLE IF NOT EXISTS `tipopintura` (
  `idTipoPintura` int(11) NOT NULL AUTO_INCREMENT,
  `NombreTipoPintura` varchar(100) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idTipoPintura`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.tiposervicio
CREATE TABLE IF NOT EXISTS `tiposervicio` (
  `idTipoServicio` int(11) NOT NULL AUTO_INCREMENT,
  `NombreTipo` varchar(100) NOT NULL,
  `idServicio` int(11) DEFAULT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idTipoServicio`),
  KEY `IX_Relationship1` (`idServicio`),
  CONSTRAINT `FK_TipoServicio_Servicio` FOREIGN KEY (`idServicio`) REFERENCES `servicio` (`idServicio`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.tipovehiculo
CREATE TABLE IF NOT EXISTS `tipovehiculo` (
  `idTipoVehiculo` int(11) NOT NULL AUTO_INCREMENT,
  `NombreTipoVehiculo` varchar(150) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idTipoVehiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.vehiculoinventario
CREATE TABLE IF NOT EXISTS `vehiculoinventario` (
  `idVehiculoInventario` int(11) NOT NULL AUTO_INCREMENT,
  `CantidadRequerida` decimal(10,2) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `idTipoVehiculo` int(11) DEFAULT NULL,
  `idInventario` int(11) DEFAULT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`idVehiculoInventario`),
  KEY `IX_Relationship4` (`idTipoVehiculo`),
  KEY `IX_Relationship5_VI` (`idInventario`),
  CONSTRAINT `FK_VehiculoInventario_Inventario` FOREIGN KEY (`idInventario`) REFERENCES `inventario` (`idInventario`),
  CONSTRAINT `FK_VehiculoInventario_TipoVehiculo` FOREIGN KEY (`idTipoVehiculo`) REFERENCES `tipovehiculo` (`idTipoVehiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla taller_pintura.venta
CREATE TABLE IF NOT EXISTS `venta` (
  `idVenta` int(11) NOT NULL AUTO_INCREMENT,
  `idCliente` varchar(50) DEFAULT NULL,
  `FechaVenta` datetime NOT NULL DEFAULT current_timestamp(),
  `TotalVenta` decimal(10,2) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted` tinyint(1) NOT NULL,
  `noTransaccion` int(11) DEFAULT NULL,
  PRIMARY KEY (`idVenta`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
