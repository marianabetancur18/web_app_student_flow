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


  return (
    <section className="status" id="status">
        <Container>
            <h1>Status académico del estudiante</h1>
            
            <h2> <img src={porcentaje} alt="Image" align="right" /> Porcentaje de avance</h2> <br></br>
            
            <p>Su porcentaje de avance es: </p>

            <h2><img src={libro} alt="Image" align="right" />Materias cursadas</h2>
            
            <p> Las materias que usted ha cursado son: </p>
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">código</th>
                  <th scope="col">Materia</th>
                  <th scope="col">Periodo</th>
                  <th scope="col">Nota</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">321311</th>
                  <td>Requisitos</td>
                  <td>2020</td>
                  <td>5</td>
                </tr>
                <tr>
                  <th scope="row">2003232</th>
                  <td>Calculo Diferencial</td>
                  <td>2018</td>
                  <td>4.7</td>
                </tr>
                <tr>
                  <th scope="row">2000323</th>
                  <td>2018</td>
                  <td>Calculo Integral</td>
                  <td>3.5</td>
                </tr>
              </tbody>
            </table> 
            
            <h2> <img src={libros} alt="Image" align="right" /> Materias faltantes</h2>
            
            <p>Las materias que faltan por cursar son: </p>
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">código</th>
                  <th scope="col">Materia</th>
                 
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">30002</th>
                  <td>Int artificial</td>
                  
                </tr>
                <tr>
                  <th scope="row">3003232</th>
                  <td>Seminario 3</td>
                  
                </tr>
                
              </tbody>
            </table> 
            

        </Container>
    </section>
  )
}
