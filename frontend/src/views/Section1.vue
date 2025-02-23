<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Section 1: API</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" sm="6">
        <v-select v-model="selectedTable" :items="tables" label="Select the name of the table" outlined></v-select>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" sm="8">
        <v-btn-toggle v-model="actionType" mandatory>
          <v-btn value="view" depressed style="background-color: #bed732;">See table</v-btn>
          <v-btn value="load" depressed style="background-color: #bed732;">Load CSV</v-btn>
          <v-btn value="delete" depressed style="background-color: #bed732;">Delete table</v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>

    <v-row v-if="actionType === 'load'">
      <v-col cols="12" sm="6">
        <v-file-input
          label="Select CSV file (1 up to 1000 rows) with one request"
          accept=".csv"
          v-model="selectedFile"
          outlined
          @change="handleFileChange"
        />
        <!-- Mostrar el nombre del archivo si existe -->
        <div v-if="selectedFileName">
          Archivo seleccionado: {{ selectedFileName }}
        </div>
        <h3>Response:</h3>
        <div>
          <v-alert
            type="success"
            v-if="tableData && tableData.message"
            border="start"
            elevation="1"
          >
            <strong>Message:</strong> {{ tableData.message }}
          </v-alert>

          <!-- Mensaje de error -->
          <v-alert
            type="error"
            v-if="tableData && tableData.detail"
            border="start"
            elevation="1"
          >
            <strong>Message:</strong> {{ tableData.detail }}
          </v-alert>
          </div>
      </v-col>
    </v-row>

    <v-row v-if="errorMessage">
      <v-col cols="12">
        <v-alert type="error" dense text>
          {{ errorMessage }}
        </v-alert>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-btn style="background-color: #bed732;" @click="handleAction">
          Execute
        </v-btn>
      </v-col>
    </v-row>

    <v-row v-if="actionType === 'view' && tableData">
      <v-col cols="12">
        <h3>Table content:</h3>
        <v-data-table 
          :headers="tableHeaders" 
          :items="tableData.data"
          :items-per-page="10"
          class="elevation-1"
        >
          <template v-slot:no-data>
            <v-alert v-if="actionExecuted" type="info" border="start" color="#bed732" elevation="1">
              No data available.
            </v-alert>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <v-row v-if="actionType === 'delete' && tableData">
      <v-col cols="12">
        <h3>Response:</h3>
        <v-alert type="info" border="start" color="#bed732" elevation="1">
          <div>
            <strong>Table:</strong> {{ tableData.table }}
          </div>
          <div>
            <strong>Rows deleted:</strong> {{ tableData.rows_deleted }}
          </div>
          <div>
            <strong>Message:</strong> {{ tableData.message }}
          </div>
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Section01",
  data() {
    return {
      selectedTable: "",
      tables: ["departments", "jobs", "employees"],
      actionType: "view",
      selectedFile: null,
      selectedFileName: "",
      fileLines: 0,
      errorMessage: "",
      tableData: { data: [] },
      headers: [],
      actionExecuted: false
    };
  },
  computed: {
    tableHeaders() {
      if (this.headers.length > 0) {
        return this.headers;
      } else {
        return [{ text: "ID", value: "id" }, { text: "Name", value: "name" }];
      }
    }
  },
  methods: {
    handleFileChange(event) {
      console.log("Evento: ", event)
      const file = this.selectedFile;
      try {
        if (!file) {
          throw new Error("No file selected.")
        };
        console.log("archivo cargado: ", file);
        if (!(file instanceof File)) {
          throw new Error("The selected file is not a valid file.");
        };

        if (file.type !== "text/csv") {
          console.warn("El archivo no tiene MIME type text/csv, es:", file.type);
        };

        // Leer el contenido como texto
        const reader = new FileReader();
        reader.onload = e => {
          const text = e.target.result;
          console.log("Contenido CSV:", text);
          // Aquí puedes procesar el CSV, contar líneas, etc.
        };
        reader.onerror = err => {
          throw new Error("Error reading file: " + err);
        };

        reader.readAsText(file);

      } catch (error) {
        console.error(error);
        // Si usas una variable para mostrar errores en el template
        this.errorMessage = error.message;
      }
    },
    async handleAction() {
      this.errorMessage = "";
      this.tableData = { data: [] };
      this.headers = []; // Reiniciar encabezados antes de consultar datos

      if (this.actionType === "view") {
        try {
          const response = await fetch(`http://localhost:8080/api/view?table_name=${this.selectedTable}`);
          if (!response.ok) {
            throw new Error("Error getting data from table");
          }
          const data = await response.json();
          this.tableData = data;

          // Generar los encabezados
          if (data.data.length > 0) {
            this.headers = Object.keys(data.data[0]).map(key => ({
              title: key.charAt(0).toUpperCase() + key.slice(1),
              key: key
            }));
          }

          console.log(this.headers)
          console.log(this.tableData)

          this.$forceUpdate();
        } catch (error) {
          this.errorMessage = error.message;
        }
      } 
      else if (this.actionType === "load") {
        if (!this.selectedFile) {
          this.errorMessage = "You must select a valid CSV file.";
          return;
        }
        const formData = new FormData();
        formData.append("tableName", this.selectedTable);
        formData.append("file", this.selectedFile);

        console.log(this.selectedTable)

        try {
          const response = await fetch(`http://localhost:8080/api/load/${this.selectedTable}`, {
            method: "POST",
            body: formData,
          });
          // if (!response.ok) {
          //   throw new Error("Error loading file");
          // }
          this.tableData = await response.json();
          console.log(this.tableData)
          this.$forceUpdate();
        } catch (error) {
          this.errorMessage = error.message;
        }
      } else if (this.actionType === "delete") {
        try {
          const response = await fetch(`http://localhost:8080/api/delete?table_name=${this.selectedTable}`, {
            method: "DELETE",
          });
          if (!response.ok) {
            throw new Error("Error deleting table information");
          }
          this.tableData = await response.json();
          console.log(this.tableData);
          this.$forceUpdate();
        } catch (error) {
          this.errorMessage = error.message;
        }
      };
      this.actionExecuted = true
    }
  }
};
</script>

<style scoped>
/* .v-data-table__th {
  color: black !important;
  font-weight: bold;
} */
</style>
