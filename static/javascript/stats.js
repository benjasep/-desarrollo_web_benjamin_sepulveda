const getDatos = async () => {
    try {
        const response = await fetch(`${window.origin}/stats`);
        const data = await response.json();
        return data;
    } catch (error) {
        return null;
    }
};

const procesarDatos1 = (data) => {
    if (!data) return [];

    const acumulado = {};
    data.forEach(item => {
        const fecha = new Date(item.fecha).getTime();
        acumulado[fecha] = (acumulado[fecha] || 0) + item.cantidad; // += item.cantidad 
    });

    const resultado = [];
    for (let fecha in acumulado) {
        resultado.push([parseInt(fecha), acumulado[fecha]]);
    }

   return resultado;

};

const procesarDatos2 = (data) => {
    if (!data) return [];

    let perrosCantidad = 0;
    let gatosCantidad = 0;

    data.forEach(item => {
        if (item.tipo === 'perro') {
            perrosCantidad += item.cantidad;
        } else if (item.tipo === 'gato') {
            gatosCantidad += item.cantidad;
        }
    });

    return [
        { name: 'Perros', y: perrosCantidad },
        { name: 'Gatos', y: gatosCantidad }
    ];
};

const procesarDatos3 = (data) => {
    if (!data) return [];
    
    const datosPorMes = data.reduce((acc, item) => {
        const fecha = new Date(item.fecha);
        const mes = fecha.toLocaleString('es-ES', { month: 'long' });
        if (!acc[mes]) {
            acc[mes] = { perros: 0, gatos: 0 };
        }
        if (item.tipo === 'perro') {
            acc[mes].perros += item.cantidad;
        } else if (item.tipo === 'gato') {
            acc[mes].gatos += item.cantidad;
        }
        return acc;
    }, {});

    const meses = [];
    const perros = [];
    const gatos = [];

    for (let mes in datosPorMes) {
        meses.push(mes);
        perros.push(datosPorMes[mes].perros);
        gatos.push(datosPorMes[mes].gatos);
    }

    return {
        categorias: meses,
        perros: perros,
        gatos: gatos   
    };
};


const crearGrafico1 = async () => {
    try {
        const data = await getDatos();
        if (!data) {
            throw new Error('No hay datos');
        }

        const adopciones = procesarDatos1(data);
        if (adopciones.length === 0) {
            throw new Error('no se procesaron datos');
        }

        Highcharts.chart('container', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Adopciones de mascotas por día'
            },
            xAxis: {
                type: 'datetime',
                title: {
                    text: 'Fecha'
                }
            },
            yAxis: {
                title: {
                    text: 'Cantidad de adopciones'
                },
                min: 0
            },
            tooltip: {
                xDateFormat: '%d/%m/%Y',
                shared: true,
                valueDecimals: 0
            },
            series: [{
                name: 'Adopciones',
                data: adopciones,
                color: '#FF9900'
            }],
            legend: {
                enabled: true
            }
        });

    } catch (error) {
        console.error('Error al crear el gráfico:', error);
    }
};


const crearGrafico2 = async () => {
    try {
        data = await getDatos();
        datosprocesados = procesarDatos2(data);

        if (!datosprocesados) {
            throw new Error('no se pudieron procesar los datos');
        }

    Highcharts.chart('container2', {
            chart: {
                type: 'pie'
            },
            title: {
                text: 'Adopciones perros vs gatos'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                name: 'Mascotas',
                colorByPoint: true,
                data: datosprocesados
            }]
        });

    } catch (error) {
        console.error('Error al crear el gráfico:', error);
    }
};

const crearGrafico3 = async () => {
    try {
        const data = await getDatos();
        const datosprocesados = procesarDatos3(data);

        if (!datosprocesados) {
            throw new Error('no se procesaron datos');
        }

        Highcharts.chart('container3', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Adopciones perro vs gatos en Meses'
            },
            xAxis: {
                categories: datosprocesados.categorias,
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Cantidad de mascotas'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [{
                name: 'Perros',
                data: datosprocesados.perros,
                color: '#FF9900'
            },{
                name: 'Gatos',
                data: datosprocesados.gatos,
                color: '#0099FF'
            }]
        });

    } catch (error) {
        console.error('Error al crear el gráfico:', error);
    }
};


crearGrafico1();
crearGrafico2();
crearGrafico3();
