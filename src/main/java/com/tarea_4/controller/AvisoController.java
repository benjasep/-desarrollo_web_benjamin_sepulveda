package com.tarea_4.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.tarea_4.model.*;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/avisos")
public class AvisoController {
    @Autowired
    private AvisosRepository avisosRepository;

    @GetMapping("/all")
    @ResponseBody
    Iterable<Avisos> getAllAvisos() {
       return avisosRepository.findAll();
    }
}
