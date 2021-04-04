import Simulator from '../src/plugins/simulator'

describe('Simulator work as expected', () => {
    test('should_work', () => {
        const simulator = new Simulator()
        expect(simulator).not.toBeNull()
    })

    test('empty', () => {
        const simulator = new Simulator()
        expect(simulator.commissionTotal).toBe(0)
        expect(simulator.profit).toBe(0)
        expect(simulator.performance).toBe(0)
        expect(simulator.operations.length).toBe(0)
    })

    test('buy_work', () => {
        const simulator = new Simulator()
            .setBrokerCommission(0)
            .setStartMoney(100)
            .setLotSize(1)

        const date = new Date(2000, 10, 10)
        simulator.buy(date, 100)
        expect(simulator.operations.length).toBe(1)

        const op = simulator.operations[0]
        const expectOp = {
            time: date,
            type: "buy",
            count: 1,
            price: 100,
            commission: 0,
            value: 100,
            change: -100,
        }

        expect(op).toEqual(expectOp)
    })

    test('sell_work', () => {
        const simulator = new Simulator()
            .setBrokerCommission(0)
            .setStartMoney(100)
            .setLotSize(1)

        const date = new Date(2000, 10, 10)
        const date2 = new Date(2000, 10, 11)
        simulator.buy(date, 100)
        simulator.sell(date2, 100)
        expect(simulator.operations.length).toBe(2)

        const op = simulator.operations[1]
        const expectOp = {
            time: date2,
            type: "sell",
            count: 1,
            price: 100,
            commission: 0,
            value: 100,
            change: 100,
        }

        expect(op).toEqual(expectOp)
    })


    test('comission_work', () => {
        const simulator = new Simulator()
            .setBrokerCommission(3.5)
            .setStartMoney(100)
            .setLotSize(1)

        const date = new Date(2000, 10, 10)
        const date2 = new Date(2000, 10, 11)
        simulator.buy(date, 50)
        const op = simulator.operations[0]
        const expectOp = {
            time: date,
            type: "buy",
            count: 1,
            price: 50,
            commission: 1.75,
            value: 98.25,
            change: -51.75,
        }

        simulator.sell(date2, 100)
        const op2 = simulator.operations[1]
        const expectOp2 = {
            time: date2,
            type: "sell",
            count: 1,
            price: 100,
            commission: 3.5,
            value: 144.75,
            change: 96.5,
        }

        expect(op2).toEqual(expectOp2)
    })

    test('lot_size_work', () => {
        const simulator = new Simulator()
            .setBrokerCommission(0)
            .setStartMoney(99)
            .setLotSize(10)
        const date = new Date(2000, 10, 10)
        simulator.buy(date, 5)
        const op = simulator.operations[0]
        const expectOp = {
            time: date,
            type: "buy",
            count: 10,
            price: 5,
            commission: 0,
            value: 99,
            change: -50,
        }

        expect(op).toEqual(expectOp)

        const date2 = new Date(2000, 10, 10)
        simulator.sell(date2, 5)
        const op2 = simulator.operations[1]
        const expectOp2 = {
            time: date2,
            type: "sell",
            count: 10,
            price: 5,
            commission: 0,
            value: 99,
            change: 50,
        }

        expect(op2).toEqual(expectOp2)
    })

    test('reset_work', () => {
        const simulator = new Simulator()
        simulator.buy(new Date(), 1)
        simulator.reset()
        expect(simulator.commissionTotal).toBe(0)
        expect(simulator.profit).toBe(0)
        expect(simulator.performance).toBe(0)
        expect(simulator.operations.length).toBe(0)
    })

    test('commission_total_work', () => {
        const simulator = new Simulator()
            .setStartMoney(101)
            .setBrokerCommission(0.05)
            .setLotSize(1)
        simulator.buy(new Date(), 100)
        simulator.sell(new Date(), 100)
        expect(simulator.commissionTotal).toBe(0.1)
    })

    test('profit_work', () => {
        const simulator = new Simulator()
            .setStartMoney(101)
            .setBrokerCommission(1)
            .setLotSize(1)
        simulator.buy(new Date(), 100)
        simulator.sell(new Date(), 200)
        expect(simulator.profit).toBe(97)
    })

    test('performance_work', () => {
        const simulator = new Simulator()
            .setStartMoney(101)
            .setBrokerCommission(1)
            .setLotSize(1)
        var dateStart = new Date(2010, 1, 1)
        var dateEnd = new Date(2011, 1, 1)
        simulator.buy(dateStart, 100)
        simulator.sell(dateEnd, 200)

        // 101 -> 198
        expect(simulator.performance).toBe(96.04)
    })
})