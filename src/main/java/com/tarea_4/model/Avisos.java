package com.tarea_4.model;


import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.JoinColumn;
import java.time.LocalDateTime;
import java.util.List;
import jakarta.persistence.Table;
import jakarta.persistence.Column;

@Entity
@Table(name = "aviso_adopcion")
public class Avisos {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name="fecha_ingreso")
    private LocalDateTime fecha;

    
    @Column(name="sector")
    private String sector;

    
    @Column(name="cantidad")
    private Integer cantidad;

    
    @Column(name="tipo")
    private String tipo;

    
    @Column(name="edad")
    private Integer edad;

    
    @JoinColumn(name = "unidad_medida")
    private String unidad_medida;

    @ManyToOne
    @JoinColumn(name = "comuna_id")
    private Comuna comuna;

    @OneToMany(mappedBy= "aviso")
    private List<Nota> notas;

    public Integer getId() {
        return id;
    }

    public LocalDateTime getFecha() {
        return fecha;
    }

    public String getSector() {
        return sector;
    }

    public Integer getCantidad() {
        return cantidad;
    }

    public String getTipo() {
        return tipo;
    }

    public Integer getEdad() {
        return edad;
    }

    public String getUnidad_medida() {
        return unidad_medida == "m" ? "meses" : "años";
    }

    public String getComuna() {
        return comuna.getNombre();
    }

    public Double getAverage() {
        if (notas == null || notas.isEmpty()) {
            return 0.0;
        }
        
        int sum = notas.stream()
                      .mapToInt(Nota::getValor)
                      .sum();
        
        return sum / (double) notas.size();
    }

    @Override
    public String toString() {
        return "Persona{" +
                "id=" + id +
                ", fecha='" + fecha + '\'' +
                ", sector='" + sector + '\'' +
                ", cantidad='" + cantidad + '\'' +
                ", tipo='" + tipo + '\'' +
                ", edad='" + edad + '\'' +
                ", comuna='" + comuna.getNombre() + '\'' +
                ", nota ='" + this.getAverage() + '\'' +
                '}';
    }

}
