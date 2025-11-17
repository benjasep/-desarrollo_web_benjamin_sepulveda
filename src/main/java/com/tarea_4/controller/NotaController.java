package com.tarea_4.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.tarea_4.model.*;

import java.util.Map;
import java.util.HashMap;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/notas")
public class NotaController {
    
    @Autowired
    private NotasRepository notaRepository;
    
    @Autowired
    private AvisosRepository avisosRepository;

    @GetMapping("/all")
    @ResponseBody
    Iterable<Nota> getAllNotas() {
       return notaRepository.findAll();
    }

    @PostMapping("/add")
    @ResponseBody
    public ResponseEntity<Map<String,String>> add(@RequestParam String aviso_id, @RequestParam String nota) {

        Double notaInt = Double.parseDouble(nota); 
        if (notaInt >= 1.0 && notaInt <= 7.0 && notaInt % 1 == 0 ){
        try {
        Avisos aviso = avisosRepository.findById(Integer.parseInt(aviso_id)) 
        .orElseThrow(() -> new RuntimeException(" Aviso no encontrado"));
        
        Nota newNota = new Nota();
        newNota.setAviso(aviso);
        newNota.setValor(Integer.parseInt(nota));
        notaRepository.save(newNota);

        Map<String, String> response = new HashMap<>();
        response.put("message", "la nota ha sido agregada");
        return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, String> response = new HashMap<>();
            response.put("error", e.getMessage());
            return ResponseEntity.badRequest().body(response);
        
        }} else {
            Map<String, String> response = new HashMap<>();
             response.put("error", "no se ha recibido un valor válido");
            return ResponseEntity.badRequest().body(response);
        }}
    }
