# Formål
Formålet med denne applikation er at automatisere dataudtræk fra Randers Kommunes indkøbssystem til udstilling i henholdsvist kommunens koncernfælles BI-system (SAP BO/KMD Insight) samt til kommunens klimamonitor (Apache Superset).

Nedenfor beskrives applikationens funktionalitet samt ansvar og arbejdsdeling i organisationen. 

# Funktionalitet
Nedenstående diagram giver et overblik over applikations placering i systemlandskabet. Selve applikationen hostes på Randers Kommunes Kubernetes-platform. 

``` mermaid
%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#3c3c3c',
      'primaryTextColor': '#fff',
      'primaryBorderColor': '#3c3c3c',
      'lineColor': '#F8B229',
      'secondaryColor': '#616161',
      'tertiaryColor': '#616161',
      'tertiaryTextColor': '#fff'
    }
  }
}%%

%% Upload af data %%
flowchart LR
    subgraph SG1["Indkøbssystem"]
        UI["Filtrerede 
            dataudtræk"] 
        FTP[("SFTP-server")] 
    end    
    subgraph SG2["Randers Kommune"]
        subgraph tom [ ]
        style tom stroke-dasharray: 0 1       
            subgraph app["Denne applikation"]
                NodeRED["Extract, transform
                og load via 
                Node-RED"]
            end
            CD["BI/SAP BO via custom
              data connectoren"]
            Klima["Randers Kommunes
              Klimamonitor"]
            evt["Evt. andre use cases"]
        end
    end
    UI-->FTP   
    FTP-->NodeRED
    NodeRED-->CD
    NodeRED-->Klima
    NodeRED-->evt

```
## *Extract*
*Extract* sker i to trin:

1. Automatiske dataudtræk opsættes i selve indkøbssystemet og filerne placeres på en SFTP-server hosted af leverandøren af indkøbssystemet.

    Det vurderes ikke hensigtsmæssigt at udtrække alle data, dels da datakvaliteten svinger inden for forskellige kategorier af varer og tjenesteydelser og dels, da datamængden er omfattende. 
    
2. Applikationen henter filerne fra SFTP-serveren.

Det skal afdækkes for hyppigt der skal kontrolleres for nye data på SFTP-serveren. Leverandøren overfører data ugentligt søndag morgen kl. 8.

## *Transform*
I det omfang der er behov, transformeres data i applikationen inden de afleveres videre.

## *Load* 
Nedenfor beskrives de forskellige *load*-scenarier. I alle tilfælde anvendes *full load* kun begrænset af de opsatte dataudtræk i indkøbssystemet, da indkøbssystemet betragtes som det autoritative register.

### Til BI/SAP BO
Til Randers Kommunes koncernfælles BI-løsning (SAP BO/KMD Insight) indlæses data via <a href="https://github.com/Randers-Kommune-Digitalisering/custom-data-connector" target=_blank>custom data connectoren</a>. Denne connector tager sig af den nødvendige transformation, så data matcher den prædefinerede syntaks, der anvendes i KMD Insight Custom Data-løsningen. 

I første omgang skal der indlæses data vedr. e-handel, men listen af datasæt forventes løbende at vokse. Applikationen kan med fordel udvikles, så det er let at tilføje flere datasæt. 

### Til Monitorering af Klimaindsatsen
Til brug i <a href="https://github.com/Randers-Kommune-Digitalisering/vis-klimadata-initiativer-aktiviteter" target=_blank>Randers Kommunes Klimamonitor</a> skal data indlæses ind i den tilhørende MariaDB-database ligeledes hosted på Kubernetes-platformen. Der skal anvendes det format, der allerede anvendes i projektet.  

I første omgang drejer det sig om brændstofdata. Det forventes, at det over tid bliver muligt at trække flere relevante data. Eksempelvis i takt med dokumentation af forskellige mærkningsordninger forbedres. 

### Til evt. andre *use cases*
I forbindelse med andre *use cases* må det forventes, at der skal udvikles andre arbejdsgange. Eventuelt både *transform* og *load*. 

# Ansvar og arbejdsdeling
## Økonomiafdelingen/Indkøb
Specificerer udtræk i indkøbssystemet og udvikler visualiseringer i front end (SAP BO/Superset). 

## IT og Digitalisering
Udvikler og drifter applikationen. I første omgang er det ligeledes IT og Digitaliserings opgave løbende at tilføje af nye dataudtræk. Over tid kan denne opgave dog flyttes til Økonomiafdelingen/Indkøb. 
