const findNewApartment = require("./findApartment")
const assert = require("chai").assert;

// Unit tests
describe("findNewApartment", function (){
    it("valid input",()=>{
        assert.throw(()=>findNewApartment.isGoodLocation(1,true), "Invalid input!")
        assert.throw(()=>findNewApartment.isGoodLocation("1",1), "Invalid input!")
    })
    it("not valid city",()=>{
        assert.equal(findNewApartment.isGoodLocation("1", true), "This location is not suitable for you.")
        assert.equal(findNewApartment.isGoodLocation("Sofia", false), "There is no public transport in area.")

    })
    it("valid city",()=>{
        assert.equal(findNewApartment.isGoodLocation("Plovdiv", true),"You can go on home tour!" )
        assert.equal(findNewApartment.isGoodLocation("Sofia", true), "You can go on home tour!" )
        assert.equal(findNewApartment.isGoodLocation("Varna", true), "You can go on home tour!" )
    })
    it("is larger enought not valid input",()=>{
        assert.throw(()=>findNewApartment.isLargeEnough("1",5),"Invalid input!");
        assert.throw(()=>findNewApartment.isLargeEnough([],5),"Invalid input!");
        assert.throw(()=>findNewApartment.isLargeEnough([1,2,3],"1"),"Invalid input!");
    })
    it("is larger enought valid input",()=>{
        assert.equal(findNewApartment.isLargeEnough([1,1,1],1),'1, 1, 1');
        assert.equal(findNewApartment.isLargeEnough([1,0,1],1),'1, 1');
        assert.equal(findNewApartment.isLargeEnough([1,2,1],1),'1, 2, 1');
    })
    it("affrodable not valid inputs",()=>{
        assert.throw(()=>findNewApartment.isItAffordable("1",5), "Invalid input!")
        assert.throw(()=>findNewApartment.isGoodLocation(11,"5"), "Invalid input!")
        assert.throw(()=>findNewApartment.isGoodLocation(-1,1), "Invalid input!")
        assert.throw(()=>findNewApartment.isGoodLocation(11,-1), "Invalid input!")
    })
    it("affrodable valid inputs",()=>{
        assert.equal(findNewApartment.isItAffordable(1,2),"You can afford this home!")
        assert.equal(findNewApartment.isItAffordable(2,1),"You don't have enough money for this house!")
        assert.equal(findNewApartment.isItAffordable(2,2),"You can afford this home!")
    })
  })