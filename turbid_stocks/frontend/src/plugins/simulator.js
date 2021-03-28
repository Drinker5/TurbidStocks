import moment from 'moment'

export default class Simulator {
    #operations = []
    #stockCount = 0
    #money = 0
    #buyHour = 23
    #sellHour = 12
    #buyMinute = 30
    #sellMinute = 0
    buyPriceOption = 'o'
    sellPriceOption = 'o'
    startMoney = 1000
    lot = 1
    brokerCommission = 0.05

    set buyTime(value) {
        this.#buyHour = value.getHours()
        this.#buyMinute = value.getMinutes()
    }
    set sellTime(value) {
        this.#sellHour = value.getHours()
        this.#sellMinute = value.getMinutes()
    }

    simulate(candles) {
        this.#operations = []
        this.#money = this.startMoney
        this.#stockCount = 0;

        for (const candle of candles) {
            var time = new Date(candle.time);
            var weekdayflag = 1 << (time.getUTCDay() - 1);
            if (
                time.getHours() == this.#buyHour &&
                time.getMinutes() == this.#buyMinute &&
                (this.buyDayFlags & weekdayflag) > 0
            )
                this.#buy(time, candle[this.buyPriceOption]);
            else if (
                time.getHours() == this.#sellHour &&
                time.getMinutes() == this.#sellMinute &&
                (this.sellDayFlags & weekdayflag) > 0
            )
                this.#sell(time, candle[this.sellPriceOption]);
        }

        return {
            operations: this.#operations,
            commission: this.#commissionTotal,
            profit: this.#profit,
            performance: this.#performance
        }
    }

    #buy(time, price) {
        // покупаем на всё
        let lotPrice = price * this.lot;
        let lotsCanBeBought = Math.trunc(this.#money / lotPrice);
        let tradePrice = lotsCanBeBought * lotPrice;
        let commission = this.#getCommission(tradePrice);
        let payment = this.#fix(tradePrice + commission);
        let count = lotsCanBeBought * this.lot;
        if (count <= 0) return;
        this.#money = this.#fix(this.#money - payment);
        this.#stockCount += count;
        let value =
            this.#fix(this.#money + this.#stockCount * price);
        this.#operations.push({
            time: time,
            type: "buy",
            count: count,
            price: price,
            commission: commission,
            value: value,
            change: -payment,
        });
    }

    #sell(time, price) {
        if (this.#stockCount <= 0) return;
        // продаём все
        let lotPrice = price * this.lot;
        let lotsCanBeSold = this.#stockCount / this.lot;
        let tradePrice = lotsCanBeSold * lotPrice;
        let commission = this.#getCommission(tradePrice);
        let refund = this.#fix(tradePrice - commission);
        let count = this.#stockCount;

        this.#money = this.#fix(this.#money + refund);
        this.#stockCount = 0;
        let value =
            this.#fix(this.#money + this.#stockCount * price);

        this.#operations.push({
            time: time,
            type: "sell",
            count: count,
            price: price,
            commission: commission,
            value: value,
            change: refund,
        });
    }

    #getCommission(val) {
        return Math.ceil(val * this.brokerCommission) / 100;
    }

    get #commissionTotal() {
        if (this.#operations.length <= 0)
            return 0;
        let result = this.#operations.reduce((a, b) => {
            return { commission: a.commission + b.commission };
        }).commission;
        return this.#fix(result * 100) / 100;
    }

    get #profit() {
        if (this.#operations.length <= 0)
            return 0;
        let lastOperation = this.operations[this.#operations.length - 1];
        let result = lastOperation.value - this.startMoney;
        return this.#fix(result * 100) / 100;
    }

    get #performance() {
        if (this.#operations.length <= 0)
            return 0;
        let start = this.#operations[0];
        let end = this.#operations[this.#operations.length - 1];
        let days = moment(end.time).diff(moment(start.time), "days");

        let startValue = start.value;
        let endValue = end.value;
        let result = (100 * (endValue / startValue - 1)) / (days / 365);
        return this.#fix(result * 100) / 100;
    }

    #fix(value) {
        return Math.round(value * 100) / 100;
    }
}