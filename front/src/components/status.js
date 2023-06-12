import { useCallback } from 'react';
import { Container, Row, Col } from "react-bootstrap";
import porcentaje from "../assets/img/porcentaje.png";
import libro from "../assets/img/libro.png";
import libros from "../assets/img/libros.png";

import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';


export const Student_status = () => {
  const cursadas = JSON.parse(sessionStorage.getItem('lista_materias_cursadas'));
  const faltantes = JSON.parse(sessionStorage.getItem('materias_faltantes'));
  const porcentaje_avance = JSON.parse(sessionStorage.getItem('porcentaje_avance'));

  console.log(faltantes.faltantes_obligatorias)

  const DisplayPorcentajesAvance=porcentaje_avance.map(
    (info)=>{
        return(
            <tr>
                <td>{info.TIPO}</td>
                <td>{info.creditos_vistos}</td>
                <td>{info.creditos_necesarios}</td>
                <td>{info.creditos_faltantes}</td>
                <td>{info.porcentaje_visto}</td>
                <td>{info.porcentaje_faltante}</td>
            </tr>
        )
    }
  )

  
  const DisplayData=cursadas.map(
    (info)=>{
        return(
            <tr>
                <td>{info.CODIGO}</td>
                <td>{info.NOMBRE}</td>
                <td>{info.CREDITOS}</td>
                <td>{info.TIPO}</td>
                <td>{info.CALIFICACION}</td>
                <td>{info.PERIODO}</td>
            </tr>
        )
    }
  )


  const DisplayDataFaltantesObligatorias= faltantes.faltantes_obligatorias .map(
    (info2)=>{
        return(
            <tr>
                <td>{info2.CODIGO}</td>
                <td>{info2.NOMBRE}</td>
                <td>{info2.CREDITOS}</td>
                <td>{info2.TIPO}</td>
                <td>{info2.PRERREQUISITOS}</td>
            </tr>
        )
    }
  )

  const DisplayDataFaltantesOptativas= faltantes.faltantes_optativas.map(
    (info2)=>{
        return(
            <tr>
                <td>{info2.CODIGO}</td>
                <td>{info2.NOMBRE}</td>
                <td>{info2.CREDITOS}</td>
                <td>{info2.TIPO}</td>
                <td>{info2.PRERREQUISITOS}</td>
            </tr>
        )
    }
  )





  return (
    <section className="status" id="status">
        <Container>
            <h1>Status académico del estudiante</h1>
            
            <h2> <img src={porcentaje} alt="Image" align="right" /> Porcentaje de avance</h2> <br></br>
            
            <p>Su porcentaje de avance es: </p>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <td>TIPO</td>
                        <td>creditos_vistos</td>
                        <td>creditos_necesarios</td>
                        <td>creditos_faltantes</td>
                        <td>porcentaje_visto</td>
                        <td>porcentaje_faltante</td>
                    </tr>
                </thead>
                <tbody>
                 
                    
                    {DisplayPorcentajesAvance}
                    
                </tbody>
            </table>

            <h2><img src={libro} alt="Image" align="right" />Materias cursadas</h2>
            
            <p> Las materias que usted ha cursado son: </p>
            
            <table class="table table-striped">
                <thead>
                    <tr>
                    <th>Codigo</th>
                    <th>Nombre</th>
                    <th>Creditos</th>
                    <th>Tipo</th>
                    <th>Calificaciones</th>
                    <th>Periodo</th>
                    </tr>
                </thead>
                <tbody>
                 
                    
                    {DisplayData}
                    
                </tbody>
            </table>
            
            <h2> <img src={libros} alt="Image" align="right" /> Materias faltantes</h2>
            
            <h3>Las materias obligatorias que faltan por cursar son: </h3>
            <table class="table">
              <thead>
                    <tr>
                    <th>Codigo</th>
                    <th>Nombre</th>
                    <th>Creditos</th>
                    <th>Tipo</th>
                    <th>Prerrequisitos</th>
                    </tr>
                </thead>
                <tbody>
                 
                    
                    {DisplayDataFaltantesObligatorias}
                    
                </tbody>
            </table> 

            <h3>Las materias optativas que faltan por cursar son: </h3>
            <table class="table">
              <thead>
                    <tr>
                    <th>Codigo</th>
                    <th>Nombre</th>
                    <th>Creditos</th>
                    <th>Tipo</th>
                    <th>Prerrequisitos</th>
                    </tr>
                </thead>
                <tbody>
                 
                    
                    {DisplayDataFaltantesOptativas}
                    
                </tbody>
            </table> 
            

        </Container>
    </section>
  )
}
