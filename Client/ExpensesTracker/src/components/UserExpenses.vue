<!-- TODO: catch all promise responses -->
<template>
    <!-- TODO: break things down to components -->
    <div>
        <div class="UserNotLoggedIn" v-if="!this.$parent.isLoggedIn">
            <p>you are not a logged in user. please,click <a href="#" v-on:click="RedirectToLogin">here</a> to login.</p>
        </div>
        <!-- TODO: change this to else statement -->
        <div v-if="this.$parent.isLoggedIn" >
            <div style="margin: 0 auto;width: 25%">
            <!-- view control -->
                <!-- <nav class="navbar navbar-expand-lg navbar-light" >
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav mr-auto">
                            <li v-for="tab in tabs" v-bind:key="tab.name">
                                <a class="nav-link" v-on:click="ChangeState(tab.stateName)" v-bind:class="{active: state == tab.stateName}" >{{tab.name}}</a>
                            </li>
                        </ul>
                    </div>
                </nav> -->
            </div>

             
            <!-- all expenses manager -->
            <div v-if="state == viewStates.expenses">
                <!-- add expenses -->
                <button class="btn btn-primary addExpensesButton" @click="ClearNewRecord" v-b-modal.modalAdd>+ Add</button>

                <!-- list all expenses -->
                <b-table 
                    v-if="allUserExpenses.length > 0" 
                    id="UserExpensesTable"
                    striped 
                    hover
                    :per-page="perPage"
                    :current-page="currentPage"
                    :items="allUserExpensesFiltered"
                    :fields="expensesTableFields">
                    >
                        <template slot="actions" slot-scope="cell">
                        <!-- We use click.stop here to prevent a 'row-clicked' event from also happening -->
                            <b-btn class="btn btn-success" size="sm" @click.stop="TargetToEdit(cell.item,cell.index,$event.target)" v-b-modal.modalAdd>Edit</b-btn>
                            <b-btn class="btn btn-danger sharp" size="sm" @click.stop="TargetToDelete(cell.item,cell.index,$event.target)" v-b-modal.modalRemove>Delete</b-btn>
                        </template>
                </b-table>
                <p v-else>No Expenses to show</p>
                <b-row>
                    <b-col md="6">
                        <b-pagination :total-rows="totalRows" :per-page="perPage" v-model="currentPage" />
                    </b-col>
                </b-row>


                <!-- Modal Remove Component -->
                <b-modal id="modalRemove" title="Confirmation" @ok="DeleteTarget">
                    <p>are you sure you want to delete this item?</p>
                </b-modal>

                <!-- Modal Add/Edit Component -->
                <b-modal id="modalAdd" title="Add New Record" ok-title="Save" @ok="AddOrEditTarget">
                    <!-- TODO create generic form -->
                    <label>Payment Date</label><input class="form-control" type="date" v-model="newRecord.PaymentDate"><br/>
                    <label>Payment Reason</label><input class="form-control" type="text" v-model="newRecord.PaymentReason"><br/>
                    <label>Payment Value</label><input class="form-control" type="number" v-model="newRecord.PaymentValue"><br/>
                    <label>Payment Currency</label>
                    <select class="form-control selectpicker bs-select" v-model="newRecord.PaymentCurrency">
                        <option
                            value=""
                            disabled>
                            -- Please select a currency --
                        </option>
                        <option
                            v-for="option in currencies"
                            :key="option.Id"
                            :value="option">
                            {{option.CurrencySlug}}
                        </option>
                    </select>
                    <label>Payment Category</label>
                    <select class="form-control selectpicker bs-select" v-model="newRecord.PaymentCategory">
                        <option
                            value=""
                            disabled>
                            -- Please select a category --
                        </option>
                        <option
                            v-for="option in categories"
                            :key="option.Id"
                            :value="option">
                            {{option.CategoryName}}
                        </option>
                    </select>
                </b-modal>
            </div>
        </div>
    </div>
</template>

<script>
import user from './../models/user'
import record from './../models/record'
import {SendPostRequest, SendGetRequest, SendDeleteRequest, SendPutRequest} from './../services/Rest'

export default {
  name: 'UserExpenses',
  data: function(){
      return {
        state: {
            type: String,
            default: "expenses"
        },
        viewStates: {
            expenses: "expenses",
            account: "account",
            currencies: "currencies",
            categories: "categories",
        },
        tabs: [
            { stateName: 'expenses', name: "Expenses"}, 
            { stateName: 'categories', name: "Categories"}, 
            { stateName: 'currencies', name: "Currencies"},
            { stateName: 'account', name: "Account"}
        ],
        
        // expenses
        expensesTableFields: ["PaymentDate", "PaymentReason", "PaymentValue", "PaymentCurrency", "PaymentCategory", "IsIncome", "actions"],
        allUserExpenses: [],
        newRecord: new record(),
        categories: [],
        currencies: [],
        
        // pagination
        totalRows: 0,
        perPage: 10,
        currentPage: 0,

        // delete, add, insert
        targetToDelete: null,
        targetToEdit: null,
      }
  },
  methods:{
      RedirectToLogin: function () {
          this.$parent.ChangeState('login')
      },
      ChangeState: function (newState) {
          this.state = newState;
          if (this.state == "expenses"){
            SendGetRequest('/record/').then((response) => {
                        this.allUserExpenses = response.body
                        this.totalRows = this.allUserExpenses.length;
            });
          }
      },
      TargetToDelete: function(item, index, eventTarget) {
          this.targetToDelete = item.Id
      },
      TargetToEdit: function (item, index, eventTarget) {
          var id = item.Id;
          let candidateExpenses = this.allUserExpenses.filter(ex => ex.Id == id);
          if(candidateExpenses.length == 0){
              // TODO display error
              console.log("unlikely error")
              return
          }
          this.targetToEdit = candidateExpenses[0];
          this.newRecord = this.targetToEdit;
      },
      DeleteTarget: function () {
          SendDeleteRequest(`/record/${this.targetToDelete}`)
            .then(response => {
                this.allUserExpenses.filter((item, idx) => {
                    if (item.Id == this.targetToDelete){
                        this.allUserExpenses.splice(idx, 1);
                        this.totalRows = this.allUserExpenses.length;
                    }
                })
            this.targetToDelete = null;
          })
      },
      AddOrEditTarget: function (event) {
          if (this.newRecord.Id != null){
            SendPutRequest('/record/', this.newRecord).then(response => {
                this.newRecord = new record()
            })
          }
          else {
            SendPostRequest('/record/', this.newRecord).then(response => {
                this.allUserExpenses.push(this.newRecord)
                this.newRecord = new record()
            })
          }   
      },
      ClearNewRecord: function () {
          this.newRecord = new record()
      }
  },
  computed:{
      allUserExpensesFiltered: function(){
          return this.allUserExpenses.map(record => {return {
              Id: record.Id,
              PaymentDate: record.PaymentDate,
              PaymentReason: record.PaymentReason,
              PaymentValue: record.PaymentValue,
              PaymentCurrency: record.PaymentCurrency.CurrencySlug,
              PaymentCategory: record.PaymentCategory.CategoryName,
              IsIncome: record.IsIncome
          }});
      },
      currencySelectionComputed: function() {
          var newList = []
          this.currencies.foreach(element => { 
              newList.append({text: element.CurrencySlub, value: element.Id})
            })
          return newList
      }
  },
  created: function () {
    if (this.$parent.isLoggedIn){
        SendGetRequest('/record/').then((response) => {
            this.allUserExpenses = response.body
            this.endIdx = this.recordsPerPage
            this.numPages = this.allUserExpenses.length / this.recordsPerPage
            this.currentPageRecords = this.allUserExpenses.slice(this.beginIdx, this.endIdx)
        });
        SendGetRequest('/category/').then((response) => {
            this.categories = response.body
        })
        SendGetRequest('/currency/').then((response) => {
            this.currencies = response.body
        })
        this.ChangeState(this.viewStates.expenses);
    }
  }
}
</script>

<style scoped>

.UserNotLoggedIn
{
    text-align: center;
}

.addExpensesButton
{
    float:right;
    margin-bottom: 2vh;
}

#UserExpensesTable
{
    border: none
}
</style>
