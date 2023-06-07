import { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import contactImg from "../assets/img/contact-img.svg";
import 'animate.css';
import TrackVisibility from 'react-on-screen';
import { Await, useNavigate } from 'react-router-dom';
import axios from 'axios'


export const Contact = () => {

  const navigate = useNavigate();
  const [buttonText, setButtonText] = useState('Send');
  const [status, setStatus] = useState({});
  const [selectedFile, setSelectedFile] = useState(null);

  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    sessionStorage.setItem('file', selectedFile)
    //const body_data = await toBase64(selectedFile)
    console.log(selectedFile)
    const formData = new FormData()
    formData.append('file', selectedFile)
    console.log(Object.entries(formData))
    let response = await axios.post("http://localhost:8000/history", formData, {
      headers: {
        'Content-Type': "multipart/form-data",
      }
    })
    sessionStorage.setItem('general_response', JSON.stringify(response.data));
    console.log(response.data);
    sessionStorage.setItem('grafo_materias_cursadas', JSON.stringify(response.data.lista_materias_cursadas));
    sessionStorage.setItem('grafo_pensum', JSON.stringify(response.data.grafo_pensum));
    sessionStorage.setItem('lista_materias_cursadas', JSON.stringify(response.data.lista_materias_cursadas));
    sessionStorage.setItem('materias_faltantes', JSON.stringify(response.data.materias_faltantes));
    sessionStorage.setItem('porcentaje_avance', JSON.stringify(response.data.porcentaje_avance));
    sessionStorage.setItem('estimado_semestres_faltantes', JSON.stringify(response.data.estimado_semestres_faltantes));
    setButtonText("Sending...");
    setButtonText("Send");
    navigate('/Actions');
  };

  return (
    <section className="contact" id="connect">
      <Container>
        <Row className="align-items-center">
          <Col size={12} md={6}>
            <TrackVisibility>
              {({ isVisible }) =>
                <img className={isVisible ? "animate__animated animate__zoomIn" : ""} src={contactImg} alt="Contact Us" />
              }
            </TrackVisibility>
          </Col>
          <Col size={12} md={6}>
            <TrackVisibility>
              {({ isVisible }) =>
                <div className={isVisible ? "animate__animated animate__fadeIn" : ""}>
                  <h2>Sube tu historia academica para acceder a todas las interacciones!</h2>
                  <form onSubmit={handleSubmit}>
                    <Row>
                      <Col size={12} sm={13} className="px-1">
                        <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} />
                      </Col>
                      <Col size={12} className="px-1">
                        <button type="submit"><span>{buttonText}</span></button>
                      </Col>
                      {
                        status.message &&
                        <Col>
                          <p className={status.success === false ? "danger" : "success"}>{status.message}</p>
                        </Col>
                      }
                    </Row>
                  </form>
                </div>}
            </TrackVisibility>
          </Col>
        </Row>
      </Container>
    </section>
  )
}
