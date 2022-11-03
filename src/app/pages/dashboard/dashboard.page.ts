import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Chart } from "chart.js";
  

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage {
@ViewChild("barCanvas", {static:true}) public barCanvas:ElementRef;
@ViewChild("doughnutCanvas", {static:true}) doughnutCanvas: ElementRef;
@ViewChild("barcanvas" ,{ static:true}) barcanvas: ElementRef;
barChart:any;
doughnutChart:any;
lineChart:any;
  constructor() { }
  ionViewWillEnter(){
    this.barChartMethod()
    this.doughnutChartMethod()
    this.barchart2()
  }
    
   barChartMethod(){
    this.barChart = new Chart(this.barCanvas.nativeElement,{
      type:'bar',
      data:{
        labels:['blueberry','vanilla','chocolate','mango'],
        datasets:[{
          barPercentage:0.8,
          barThickness:'flex',
          label:"Critical",
          stack:"sensitivity",
          backgroundColor: " #ff2afa",
          data:[10,20,30,32],
        },{
          barPercentage:0.8,
          barThickness:'flex',
          label:"Current Quantity",
          stack:"sensitivity",
          backgroundColor: " #af00fe",
          data:[20,38,20,30],
        }

        ]
      },
      options:{
        scales:{
         y:{
          beginAtZero: true
         }

         

          
        }
      }
      

    })
      
   }
 doughnutChartMethod(){
  this.doughnutChart = new Chart(this.doughnutCanvas.nativeElement,{
    type: "doughnut",
      data: {
        labels: ["yogurt", "juice", "icecream",],
        datasets: [
          {
            label: "# of Votes",
            data: [12, 19, 3, ],
            borderWidth:0,
            borderRadius:1,
           
            rotation:2,
            offset:2,
            backgroundColor: [
              "#07f4ff",
              "#4afb6d",
              "#af00fe",
              
            ],
           
           
          }
        ]
      }
  }
    )
 }

barchart2(){
  this.barChart = new Chart(this.barcanvas.nativeElement,{
    type:'bar',
    data:{
      labels:['order In','order Out'],
      datasets:[{
        barPercentage:0.8,
        barThickness:'flex',
        label:"yogurt",
        stack:"Base",
        backgroundColor: "#07f4ff ",
        data:[30,20],
      },{
        barPercentage:0.8,
        barThickness:'flex',
        label:"Ice cream",
        stack:"base",
        backgroundColor: "#af00fe ",
        data:[44,38],
      },{
        barPercentage:0.8,
        barThickness:'flex',
        label:"Juice",
        stack:"sensitivity",
        backgroundColor: "#4afb6d",
        data:[70,50],
      }

      ]
    },
    options:{
      scales:{
       y:{
        beginAtZero: true
       }

       

        
      }
    }
    

  })
    
 }

        
          
        
      
  
  

  

    }
