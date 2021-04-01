import Simulator from '../src/plugins/simulator'

test('should_work', () => {
    var simulator = new Simulator()
    expect(simulator).not.toBeNull()
})

test('empty', () => {
    var simulator = new Simulator()
    expect(simulator.commissionTotal).toBe(0)
    expect(simulator.profit).toBe(0)
    expect(simulator.performance).toBe(0)
    expect(simulator.operations.length).toBe(0)
})

