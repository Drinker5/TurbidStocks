import moment from 'moment'

export default class Simulator {
    #operations = []
    #stockCount = 0
    #money = 0
    #lot = 1
    #startMoney = 1000
    #brokerCommission = 0.05
    #commissionTotal = 0
    constructor() {
        this.#money = this.#startMoney
    }

    setLotSize(lot) {
        this.#lot = lot
        return this
    }

    setBrokerCommission(brokerCommission) {
        this.#brokerCommission = brokerCommission
        return this
    }

    setStartMoney(startMoney) {
        this.#startMoney = startMoney
        return this
    }

    setBrokerCommission(brokerCommission) {
        this.#brokerCommission = brokerCommission
        return this
    }

    reset() {
        this.#operations = []
        this.#money = this.#startMoney
        this.#stockCount = 0
        this.#commissionTotal = 0
    }

    buy(time, price) {
        if (this.#operations.length == 0)
            this.reset()
        // покупаем на всё
        const lotPrice = price * this.#lot;
        const lotPriceWithCommision = lotPrice + this.#calcCommission(lotPrice)
        const lotsCanBeBought = Math.trunc(this.#money / lotPriceWithCommision);
        const tradePrice = lotsCanBeBought * lotPrice;
        const commission = this.#calcCommission(tradePrice);
        const result = this.#fix(tradePrice + commission);
        const count = lotsCanBeBought * this.#lot;
        if (count <= 0) return;
        this.#money = this.#fix(this.#money - result);
        this.#stockCount += count;
        const value =
            this.#fix(this.#money + this.#stockCount * price);

        this.#commissionTotal += commission
        this.#operations.push({
            time: time,
            type: "buy",
            count: count,
            price: price,
            commission: commission,
            value: value,
            change: -result,
        });
    }

    sell(time, price) {
        if (this.#stockCount <= 0)
            return;
        // продаём все
        const lotPrice = price * this.#lot;
        const lotsCanBeSold = this.#stockCount / this.#lot;
        const tradePrice = lotsCanBeSold * lotPrice;
        const commission = this.#calcCommission(tradePrice);
        const result = this.#fix(tradePrice - commission);
        const count = this.#stockCount;

        this.#money = this.#fix(this.#money + result);
        this.#stockCount = 0;
        const value =
            this.#fix(this.#money + this.#stockCount * price);

        this.#commissionTotal += commission
        this.#operations.push({
            time: time,
            type: "sell",
            count: count,
            price: price,
            commission: commission,
            value: value,
            change: result,
        });
    }

    #calcCommission(val) {
        return Math.ceil(val * this.#brokerCommission) / 100;
    }

    get operations() {
        return this.#operations
    }

    get commissionTotal() {
        return this.#commissionTotal
    }

    get profit() {
        if (this.#operations.length <= 0)
            return 0;
        let lastOperation = this.#operations[this.#operations.length - 1];
        let result = lastOperation.value - this.#startMoney;
        return this.#fix(result);
    }

    get performance() {
        if (this.#operations.length <= 0)
            return 0;
        let start = this.#operations[0];
        let end = this.#operations[this.#operations.length - 1];
        let days = moment(end.time).diff(moment(start.time), "days");

        let startValue = this.#startMoney;
        let endValue = end.value;
        let result = (100 * (endValue / startValue - 1)) / (days / 365);
        return this.#fix(result);
    }

    #fix(value) {
        return Math.round(value * 100) / 100;
    }
}