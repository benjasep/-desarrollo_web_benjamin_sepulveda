package com.tarea_4.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Table;
import jakarta.persistence.ManyToOne;

import jakarta.persistence.Column;

@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "aviso_id")
    private Avisos aviso;

    @Column(name ="nota")
    private Integer nota;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getValor() {
        return nota;
    }

    public void setValor(Integer nota) {
        this.nota=nota;
    }

    public Avisos getAviso() {
        return this.aviso;
    }

    public void setAviso(Avisos aviso) {
        this.aviso=aviso;
    }
}
