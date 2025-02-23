<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Section 2: SQL</h1>
        <h3>Requirements</h3>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <p>
          Number of employees hired for each job and department in 2021 divided by quarter.
          The table must be ordered alphabetically by department and job.
          <v-btn color="#bed732" @click="handleFirstQuery">Execute query</v-btn>
        </p>
        <v-row v-if="executeQuery01 === 'query_01' && tableData01">
          <v-col cols="12">
            <h3>Table content:</h3>
            <v-data-table :headers="tableHeaders01" :items="tableData01" :items-per-page="10" class="elevation-1">
              <template v-slot:no-data>
                <v-alert v-if="actionExecuted01" type="info" border="start" color="#bed732" elevation="1">
                  No data available.
                </v-alert>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
        <br>
        <p>
          List of ids, name and number of employees hired of each department that hired more employees than
          the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired
          (descending).
          <v-btn color="#bed732" @click="handleSecondQuery">Execute query</v-btn>
        </p>
        <v-row v-if="executeQuery02 === 'query_02' && tableData02">
          <v-col cols="12">
            <h3>Table content:</h3>
            <v-data-table :headers="tableHeaders02" :items="tableData02" :items-per-page="10" class="elevation-1">
              <template v-slot:no-data>
                <v-alert v-if="actionExecuted02" type="info" border="start" color="#bed732" elevation="1">
                  No data available.
                </v-alert>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
export default {
  name: "MyQueries",
  data() {
    return {
      executeQuery01: "",
      tableData01: null,
      tableHeaders01: [],
      actionExecuted01: false,
      executeQuery02: [],
      tableData02: null,
      tableHeaders02: [],
      actionExecuted02: false
    };
  },
  methods: {
    async handleFirstQuery() {
      this.executeQuery01 = "query_01";
      this.actionExecuted01 = false;
      this.tableData01 = null;

      try {

        const response = await fetch("http://localhost:8080/api/query/handleFirstQuery");
        if (!response.ok) {
          throw new Error("Error fetching Query 01");
        }
        const data = await response.json();
        this.tableData01 = data;

        if (data.length > 0) {
          this.tableHeaders01 = Object.keys(data[0]).map(key => ({
            title: key.toUpperCase(),
            key: key
          }));
        }
      } catch (error) {
        console.error(error);
      } finally {
        this.actionExecuted01 = true;
      }
    },
    async handleSecondQuery() {
      this.executeQuery02 = "query_02";
      this.actionExecuted02 = false;
      this.tableData02 = null;

      try {
        const response = await fetch("http://localhost:8080/api/query/handleSecondQuery");
        if (!response.ok) {
          throw new Error("Error fetching Query 02");
        }
        const data = await response.json();

        this.tableData02 = data;
        if (data.length > 0) {
          this.tableHeaders02 = Object.keys(data[0]).map(key => ({
            title: key.toUpperCase(),
            key: key
          }));
        }
      } catch (error) {
        console.error(error);
      } finally {
        this.actionExecuted02 = true;
      }
    }
  }
};
</script>