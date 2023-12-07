## Functional Tissue Units in the Human Reference Atlas

Supriya Bidanta<sup>1,4</sup>, Katy Börner<sup>1,4,5</sup>, Ellen M. Quardokus<sup>1</sup>, Bruce W. Herr II<sup>1</sup>, Marcell Nagy<sup>2</sup>, Katherine S. Gustilo<sup>1</sup>, Rachel Bajema<sup>1</sup>, Libby Maier<sup>1</sup>, Roland Molontay<sup>2</sup>, Griffin Weber<sup>3,5</sup>

<sup>1</sup> Indiana University, Bloomington, IN; 
<sup>2</sup> Budapest University of Technology and Economics, Budapest, Hungary;
<sup>3</sup> Harvard Medical School, Boston, MA

<sup>4</sup> Contributed equally (co-first authors)
<sup>5</sup> Corresponding authors 

Functional tissue units (FTUs) form the basic building blocks of organs and are important for understanding and modeling the healthy physiological function of the organ and changes that occur during disease states. In this first comprehensive catalog of 22 anatomically correct, nested functional tissue units (FTUs) from 10 healthy human organs, we document the definition, physical dimensions, blood vasculature connections, and cellular composition. All anatomy terms are mapped to the multi-species Uber-anatomy Ontology (UBERON) and Cell Ontology (CL) to support computational access via standardized metadata. The catalog includes datasets, illustrations, an online interactive FTU Explorer that supports exploration of published experimental datasets at single cell level, and a large printable poster illustrating how the blood vasculature connects the 22 FTUs in 10 organs. All data and code are freely available. The work is part of an ongoing international effort to construct a Human Reference Atlas (HRA) of all cells in the human body.

The repo is structured in the following way:

```
├── data
├── code
├── exploration
├── visualization
```

### Data
The data folder has the 1 supplemental table and the intestinal villus FTU in the small intestine (SVG, PNG, AI file format) together with a table that lists the different types of cells in each of the 22 FTUs which will be published with the 6th release of the HRA end of December 2023.
  
### Code
Two Python notebooks are provided. Run FTU_Explorer_data.ipynb to compile data for the Interactive FTU Explorer visualization. Run HRA_Butterfly_viz.ipynb to generate a radial tree butterfly resembling visualization of the anatomical structures partonomy with an overlay of the vasculature tree that connects the chambers of the heart in the center via increasingly smaller vessels to the 22 FTUs.

##### Prerequisite:
  - Python (version > 3.9)
  - R-studio
  - pycharm (recommended)
  - jupyter
  - packages: pyvis, networkx, datashader, scanpy  

The interactive FTU Explorer code uses single-nucleus RNA sequencing data from the <a href="https://www.ebi.ac.uk/gxa/sc/experiments?species=%22homo%20sapiens%22" target="_blank">Single Cell Expression Atlas Portal</a> for organs that have anatomograms. The reference files are used to compute gene and cell type information, Ensemble ID, HGNC gene ID, HGNC gene symbol, count and percentage of cell type, and mean expression values. This data is then converted to a JSON file that is read by the Interactive FTU Explorer.

The butterfly visualization code reads  data from the <a href="https://hubmapconsortium.github.io/ccf-asct-reporter" target="_blank">ASCT+B Reporter</a> in JSON format. It generates SVG files that can be combined and post-processed in a graphics editor like Adobe Illustrator to add a legend, title, FTUs, and any other information.

### Exploration
Two tables and two JSON files are provided for use in the Interactive FTU Explorer. Table-A has experimental data for kidney, liver, and lung together with cell count and percentage per cell type per organ. Table-B has data on cell type per gene expression matrices for 11 FTUs with percentages and mean expression values per cell type. The file named ```ftu-datasets.jsonld``` contains details about the FTU and the data source utilized for retrieving FTU data. The file ```ftu-cell-summaries.jsonld``` provides information on cell types, genes, and the average expression for each cell type.   

### Visualization
The directory features all files to view and print the 36" poster. To print the poster on a 36" printer, resize the two halves to 35.5".



  
    
