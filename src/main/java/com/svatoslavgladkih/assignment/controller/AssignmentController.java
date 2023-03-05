package com.svatoslavgladkih.assignment.controller;

import com.svatoslavgladkih.assignment.model.ReqestCheckDTO;
import com.svatoslavgladkih.assignment.service.FileComparatorService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AssignmentController {
    private final FileComparatorService comparatorService;

    public AssignmentController(FileComparatorService comparatorService) {
        this.comparatorService = comparatorService;
    }

    @PostMapping("/check")
    public String checkText(@RequestBody ReqestCheckDTO source) {
        return "result: " + comparatorService.checkSimilarity(source.getFilename(), source.getText());
    }

}
