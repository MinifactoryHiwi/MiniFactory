import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {  Chart,registerables} from "chart.js";

Chart.register(...registerables);
@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent {
  constructor(
    private router:Router
  ) {}
  goToHome(){
    this.router.navigate(['homepage'])

  }
}
