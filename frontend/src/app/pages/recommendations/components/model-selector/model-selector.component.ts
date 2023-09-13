import {Component, EventEmitter, inject, OnInit, Output} from '@angular/core';
import {ModelService} from "../../../../services/model-service";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {Model} from "../../../../models/model";

@Component({
  selector: 'app-model-selector',
  templateUrl: './model-selector.component.html',
  styleUrls: ['./model-selector.component.sass'],
  providers: [ModelService]
})
export class ModelSelectorComponent implements OnInit {
  models: string[] = [];
  algorithms: Model[] = [];
  algorithm: FormControl;
  model: FormControl;
  k: FormControl;
  @Output()
  sendAlgorithmEmitter: EventEmitter<any> = new EventEmitter();
  @Output()
  sendModelEmitter: EventEmitter<any> = new EventEmitter();
  @Output()
  sendKEmitter: EventEmitter<any> = new EventEmitter();
  private service = inject(ModelService);

  constructor() {
    this.service.getModels().subscribe(models => this.algorithms = models);
    this.algorithm = new FormControl(null, Validators.required);
    this.model = new FormControl({value: null, disabled: true}, Validators.required);
    this.k = new FormControl(null, Validators.required);

  }

  ngOnInit(): void {
    this.algorithm.valueChanges.subscribe((algorithm) => {
      this.model.reset();
      this.model.disable();
      if (algorithm) {
        this.models = this.algorithms.find(a => a.algorithm == algorithm)?.models || [];
        this.sendModelEmitter.emit('');
        this.model.enable();
      }
    });
  }

  setModel(value: any) {
    this.sendModelEmitter.emit(value.value);
  }

  setAlgorithm(value: any) {
    this.sendAlgorithmEmitter.emit(value.value);
  }

  setK(value: any) {
    this.sendKEmitter.emit(value);
  }

}
