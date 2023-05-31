import meter1 from "../assets/img/meter1.svg";
import meter2 from "../assets/img/meter2.svg";
import meter3 from "../assets/img/meter3.svg";
import meter4 from "../assets/img/meter4.svg";
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import arrow1 from "../assets/img/arrow1.svg";
import arrow2 from "../assets/img/arrow2.svg";
import colorSharp from "../assets/img/color-sharp.png"
import { useNavigate } from 'react-router-dom';

export const Actions = () => {

  const navigate = useNavigate();
  console.log(sessionStorage.getItem('file'))
  const responsive = {
    superLargeDesktop: {
      // the naming can be any, depends on you.
      breakpoint: { max: 4000, min: 3000 },
      items: 5
    },
    desktop: {
      breakpoint: { max: 3000, min: 1024 },
      items: 3
    },
    tablet: {
      breakpoint: { max: 1024, min: 464 },
      items: 2
    },
    mobile: {
      breakpoint: { max: 464, min: 0 },
      items: 1
    }
  };

  return (
    <section className="interactions" id="interactions">
        <div className="container">
            <div className="row">
                <div className="col-12">
                    <div className="interactions-bx wow zoomIn">
                        <h2>Que quieres descubrir el dia de hoy?</h2>
                        <br/>
                        <br/>
                        <Carousel responsive={responsive} infinite={true} className="owl-carousel owl-theme interactions-slider">
                            <div className="item">
                                <img src={meter1} alt="Image" onClick={() => navigate('/Progress')}/>
                                <h5>Progresos</h5>
                            </div>
                            <div className="item">
                                <img src={meter2} alt="Image" />
                                <h5>Verifica status estudiante</h5>
                            </div>
                            <div className="item">
                                <img src={meter3} alt="Image" />
                                <h5>Lista asignaturas</h5>
                            </div>
                            <div className="item">
                                <img src={meter4} alt="Image" />
                                <h5>Validación procesos</h5>
                            </div>
                        </Carousel>
                    </div>
                </div>
            </div>
        </div>
    </section>
  )
}
