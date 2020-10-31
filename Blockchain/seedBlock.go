package main

import (
	"fmt"
	"encoding/json"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	pb "github.com/hyperledger/fabric/protos/peer"
)


// Seed structure
type SeedInfo struct {
	ID string `json:"ID"`
	Owner	string `json:"owner"`
	Crop	string `json:"crop"`
	Variety	string `json:"variety"`
	SourceTagNo	string `json:"sourceTagNo"`
	SourceClass	string `json:"sourceClass"`
	DestinationClass	string `json:"destinationClass"`
	SourceQuantity	string `json:"sourceQuantity"`
	SourceDateOfIssue	string `json:"sourceDateOfIssue"`
	SpaName	string `json:"spaName"`
	SourceStoreHouse	string `json:"sourceStoreHouse"`
	DestinationStoreHouse	string `json:"destinationStoreHouse"`
	SgName	string `json:"sgName"`
	SgId	string `json:"sgId"`
	FinYear	string `json:"finYear"`
	Season	string `json:"season"`
	LandRecordsKhataNo	string `json:"landRecordsKhataNo"`
	LandRecordsPlotNo	string `json:"landRecordsPlotNo"`
	LandRecordsArea	string `json:"landRecordsArea"`
	CropRegistrationCode	string `json:"cropRegistrationCode"`
	SPPName	string `json:"sppName"`
	SPPId	string `json:"sppId"`

	SCAName string `json:"scaName"`
	TotalQuantityProduced string `json:"totalQuantityProduced"`
	ProcessingDate string `json:"processingDate"`
	VerificationDate string `json:"verificationDate"`
	SampleSecretCode string `json:"sampleSecretCode"`
	SampleTestDate string `json:"sampleTestDate"`
	CertificateNumber string `json:"certificateNumber"`
	TagSeries string `json:"tagSeries"`
	TagIssuedRangeFrom string `json:"tagIssuedRangeFrom"`
	TagIssuedRangeTo string `json:"tagIssuedRangeTo"`
	NoOfTagsIssued string `json:"noOfTagsIssued"`
	CetificateValidityInMonth string `json:"cetificateValidityInMonth"`

	StoreHouseLocation string `json:"storeHouseLocation"`
	HumidityOfStorage string `json:"humidityOfStorage"`
	TemperatureOfStorage string `json:"temperatureOfStorage"`

	STLName string `json:"stlName"`
	SamplePassed string `json:"samplePassed"`
}

type SeedUpdateCertification struct {
	SCAName string `json:"scaName"`
	TotalQuantityProduced string `json:"totalQuantityProduced"`
	ProcessingDate string `json:"processingDate"`
	VerificationDate string `json:"verificationDate"`
	SampleSecretCode string `json:"sampleSecretCode"`
	SampleTestDate string `json:"sampleTestDate"`
	CertificateNumber string `json:"certificateNumber"`
	TagSeries string `json:"tagSeries"`
	TagIssuedRangeFrom string `json:"tagIssuedRangeFrom"`
	TagIssuedRangeTo string `json:"tagIssuedRangeTo"`
	NoOfTagsIssued string `json:"noOfTagsIssued"`
	CetificateValidityInMonth string `json:"cetificateValidityInMonth"`
}

type SeedUpdateTests struct {
	STLName string `json:"stlName"`
	SamplePassed string `json:"samplePassed"`
}

type SeedUpdateDist struct {
	SourceStoreHouse	string `json:"sourceStoreHouse"`
	DestinationStoreHouse	string `json:"destinationStoreHouse"`
	StoreHouseLocation string `json:"storeHouseLocation"`
	HumidityOfStorage string `json:"humidityOfStorage"`
	TemperatureOfStorage string `json:"temperatureOfStorage"`
}

// SeedChaincode implementation of Chaincode
type SeedChaincode struct {
}

// Init of the chaincode
// This function is called only one when the chaincode is instantiated.
// So the goal is to prepare the ledger to handle future requests.
func (t *SeedChaincode) Init(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("########### SeedChaincode Init ###########")

	// Get the function and arguments from the request
	function, _ := stub.GetFunctionAndParameters()

	// Check if the request is the init function
	if function != "init" {
		return shim.Error("Unknown function call")
	}

	// // Put in the ledger the key/value hello/world
	// err := stub.PutState("hello", []byte("world"))
	// if err != nil {
	// 	return shim.Error(err.Error())
	// }

	// Return a successful message
	return shim.Success(nil)
}

// Invoke
// All future requests named invoke will arrive here.
func (t *SeedChaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("########### SeedChaincode Invoke ###########")

	// Get the function and arguments from the request
	function, args := stub.GetFunctionAndParameters()

	// Check whether it is an invoke request
	if function != "invoke" {
		return shim.Error("Unknown function call")
	}

	// Check whether the number of arguments is sufficient
	if len(args) < 1 {
		return shim.Error("The number of arguments is insufficient.")
	}

	// In order to manage multiple type of request, we will check the first argument.
	// Here we have one possible argument: query (every query request will read in the ledger without modification)
	if args[0] == "query" {
		return t.query(stub, args)
	}

	// The update argument will manage all update in the ledger
	if args[0] == "invoke" {
		return t.invoke(stub, args)
	}

	if args[0] == "updateTest" {
		return t.updateTest(stub, args)
	}

	if args[0] == "updateCertification" {
		return t.updateCertification(stub, args)
	}

	if args[0] == "updateDist" {
		return t.updateDist(stub, args)
	}

	if args[0] == "getHistory" {
		return t.getHistory(stub, args)
	}

	// If the arguments given don’t match any function, we return an error
	return shim.Error("Unknown action, check the first argument")
}

// query
// Every readonly functions in the ledger will be here
func (t *SeedChaincode) query(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	fmt.Println("########### SeedChaincode query ###########")

	// Check whether the number of arguments is sufficient
	if len(args) < 2 {
		return shim.Error("The number of arguments is insufficient.")
	}

	// Like the Invoke function, we manage multiple type of query requests with the second argument.
	// We also have only one possible argument: hello

	// Get the state of the value matching the key hello in the ledger
	state, err := stub.GetState(args[1])
	if err != nil {
		return shim.Error("Failed to get state of hello")
	}

	// Return this value in response
	return shim.Success(state)
}

// invoke
// Every functions that read and write in the ledger will be here
func (t *SeedChaincode) invoke(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	fmt.Println("########### SeedChaincode invoke ###########")

	if len(args) < 2 {
		return shim.Error("The number of arguments is insufficient.")
	}

	if len(args) == 3 {

		// Write the new value in the ledger
		var data SeedInfo
		err := json.Unmarshal([]byte(args[2]), &data)
		if err != nil {
			return shim.Error("Argument 2 was not a valid JSON")
		}

		jsonified, err := json.Marshal(data)
		if err != nil {
			return shim.Error("Failed to convert to JSON")
		}

		err = stub.PutState(args[1], jsonified)
		if err != nil {
			return shim.Error("Failed to update state of hello")
		}

		err = stub.SetEvent("eventInvoke", []byte{})
		if err != nil {
			return shim.Error(err.Error())
		}

		// Return this value in response
		return shim.Success(nil)
	}

	// If the arguments given don’t match any function, we return an error
	return shim.Error("Unknown invoke action, check the second argument.")
}

func (t *SeedChaincode) updateTest(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) < 3 {
		return shim.Error("The number of arguments is insufficient.")
	}
	if len(args) == 3 {
		var updateData SeedUpdateTests
		err := json.Unmarshal([]byte(args[2]), &updateData)
		if err != nil {
			return shim.Error("Bad JSON data")
		}

		dataJSON, err := stub.GetState(args[1])
		if err != nil {
			return shim.Error("Seed does not yet exist")
		}
		var data SeedInfo
		err = json.Unmarshal(dataJSON, &data)
		if err != nil {
			return shim.Error("bad JSON in blockchain")
		}

		data.STLName = updateData.STLName
		data.SamplePassed = updateData.SamplePassed

		dataJSON, err = json.Marshal(data)
		if err != nil {
			return shim.Error("Could not convert to JSON")
		}

		err = stub.PutState(args[1], dataJSON)
		if err != nil {
			return shim.Error("Could not write back to blockchain")
		}

		return shim.Success(nil)
	}

	return shim.Error("Bad number of arguments")
}

func (t *SeedChaincode) updateCertification(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) < 3 {
		return shim.Error("The number of arguments is insufficient.")
	}
	if len(args) == 3 {
		var updateData SeedUpdateCertification
		err := json.Unmarshal([]byte(args[2]), &updateData)
		if err != nil {
			return shim.Error("Bad JSON data")
		}

		dataJSON, err := stub.GetState(args[1])
		if err != nil {
			return shim.Error("Seed does not yet exist")
		}
		var data SeedInfo
		err = json.Unmarshal(dataJSON, &data)
		if err != nil {
			return shim.Error("bad JSON in blockchain")
		}

		data.SCAName = updateData.SCAName
		data.TotalQuantityProduced = updateData.TotalQuantityProduced
		data.ProcessingDate = updateData.ProcessingDate
		data.VerificationDate = updateData.VerificationDate
		data.SampleSecretCode = updateData.SampleSecretCode
		data.SampleTestDate = updateData.SampleTestDate
		data.CertificateNumber = updateData.CertificateNumber
		data.TagSeries = updateData.TagSeries
		data.TagIssuedRangeFrom = updateData.TagIssuedRangeFrom
		data.TagIssuedRangeTo = updateData.TagIssuedRangeTo
		data.NoOfTagsIssued = updateData.NoOfTagsIssued
		data.CetificateValidityInMonth = updateData.CertificateNumber

		dataJSON, err = json.Marshal(data)
		if err != nil {
			return shim.Error("Could not convert to JSON")
		}

		err = stub.PutState(args[1], dataJSON)
		if err != nil {
			return shim.Error("Could not write back to blockchain")
		}

		return shim.Success(nil)
	}

	return shim.Error("Bad number of arguments")
}

func (t *SeedChaincode) updateDist(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) < 3 {
		return shim.Error("The number of arguments is insufficient.")
	}
	if len(args) == 3 {
		var updateData SeedUpdateDist
		err := json.Unmarshal([]byte(args[2]), &updateData)
		if err != nil {
			return shim.Error("Bad JSON data")
		}

		dataJSON, err := stub.GetState(args[1])
		if err != nil {
			return shim.Error("Seed does not yet exist")
		}
		var data SeedInfo
		err = json.Unmarshal(dataJSON, &data)
		if err != nil {
			return shim.Error("bad JSON in blockchain")
		}

		data.SourceStoreHouse = updateData.SourceStoreHouse
		data.DestinationStoreHouse = updateData.DestinationStoreHouse
		data.StoreHouseLocation = updateData.StoreHouseLocation
		data.HumidityOfStorage = updateData.HumidityOfStorage
		data.TemperatureOfStorage = updateData.TemperatureOfStorage

		dataJSON, err = json.Marshal(data)
		if err != nil {
			return shim.Error("Could not convert to JSON")
		}

		err = stub.PutState(args[1], dataJSON)
		if err != nil {
			return shim.Error("Could not write back to blockchain")
		}

		return shim.Success(nil)
	}

	return shim.Error("Bad number of arguments")
}

func (t *SeedChaincode) getHistory(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) < 2 {
		return shim.Error("The number of arguments is insufficient.")
	}
	iter, err := stub.GetHistoryForKey(args[1])
	if err != nil {
		return shim.Error("Could not find key!")
	}
	defer iter.Close()
	var assets []SeedInfo
	for iter.HasNext() {
		dataJSON, err := iter.Next()
		if err != nil {
			return shim.Error("Could not find data from key")
		}

		var data SeedInfo
		err = json.Unmarshal(dataJSON.Value, &data)
		if err != nil {
			return shim.Error("Got invalid data from blockchain")
		}
		assets = append(assets, data)
	}

	assetsJSON, err := json.Marshal(assets)
	if err != nil {
		return shim.Error("Could not encode data to JSON")
	}

	return shim.Success(assetsJSON)
}

func main() {
	// Start the chaincode and make it ready for futures requests
	err := shim.Start(new(SeedChaincode))
	if err != nil {
		fmt.Printf("Error starting Seed Service chaincode: %s", err)
	}
}

