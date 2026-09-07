# ATLAS
*Written in the prophetic perfect tense to give myself some motivation*

ATLAS (the Atomic-scale Tunneling and Local Analysis System) is a low-cost scanning tunneling microscope (STM) build inspired by Dimsmary's OpenSTM project (https://github.com/Dimsmary/OpenSTM), with the end goal to accurately image carbon atoms on the lattice of a sample of HOPG.
## File Structure

```
\pcb
	\stm_pmod
		stm_pmod.kicad_pcb
		stm_pmod.kicad_prl
		stm_pmod.kicad_pro
		stm_pmod.kicad_sch
	\stm_psu
		stm_psu.kicad_pcb
		stm_psu.kicad_prl
		stm_psu.kicad_pro
		stm_psu.kicad_sch
	\stm_tia
		stm_tia.kicad_pcb
		stm_tia.kicad_prl
		stm_tia.kicad_pro
		stm_tia.kicad_sch
	stm_parts_lib.bak
	stm_parts_lib.kicad_sym
\code
\cad
\reference
	openstm_paper.pdf
README.md
BOM.md
LICENSE.txt
```
## How does ATLAS work?
ATLAS is a **scanning tunneling microscope** (STM). Essentially, you have a tip of some hard conductive material (Pt-Ir in this case) that is brought within nanometers of a sample, and very slowly moved along it. As the tip moves along the sample, electrons can tunnel from the atoms in the sample to the tip, which creates a miniscule current. What an STM does is take that current and through PCB wizardry amplify it into something readable, and from that construct a 3D image of the sample at the atomic scale.
# The project itself...
## A bit about this project
*For a more detailed log, refer to my blog at brentius.github.io/blog.*

I first started thinking of this project after my GCSEs in late June 2026, but I really didn't start work until September/October of that year. I'd been (very slowly) working my way through Griffths's *Introduction to Quantum Mechanics* the year before, and I thought it'd be a great idea to simply have fun and play around with quantum tunneling for a bit. I also wanted to do an actual *practical* project, because I absolutely adore PCB design - it's almost theraputic (triggers the same bits of my brain as those iPad games where you need to connect the dots without the lines crossing each other). But before I started any work, the project had to satisfy a few criteria:

1. Is it cool or not? Self explanatory, and I think I made the right choice.
2. Will it kill me? No matter how cool a project, there's not much use in doing it if I die in the process; I'd quite like to stay alive, thank you very much.
3. What can I learn from it? I've always been itching to try my hand at FPGAs, and this project was the perfect opportunity to do so.
4. How expensive will it be? At the end of the day, I don't have infinite funding; if I fry a PCB, or I break a Pt-Ir tip, it's coming out of my own pocket. Not ideal.

The only project that really satisfied all 4 criteria was building an STM, so I got to work on it. I was on vacation in Spain and Sweden during July, so there really wasn't much I could do except for starting to work on the PCBs. And my god, were these a pain.

ATLAS consists of 5 PCBs:
1. **TIA/preamp**. This uses an OPA627 DAC, along with a 100M resistor, to take in the *absolutely miniscule* current from electrons tunneling from the sample to the tip and amplify it by ~10e8 V/A, to get 15 volts running out of the back. This was actually one of the easier PCBs to design, mostly because of how few components there were. The main difficulty in designing the TIA board was physical routing - the current input trace had to be as short as possible and use as little copper as possible, and it also needed to be fenced off with the Great Wall of Vias (there's probably a Latin joke to be made in there but frankly I'm too dumb to make it) to protect it from interference from other traces. This meant that the shape of the board itself was hard to design, as the resistor meant that the board was quite large in both X and Y; considering this had to sit on the scanner block, it was not ideal.
2. **Converter/Pmod carrier**. This was about the point where I figured out I was probably extremely out of my depth. The Converter acts as a translator between the FPGA and the analog circuitry; onboard there's a SAR ADC, which takes the output from the TIA and digitises it for a PID loop. There are also two DAC8734s, that generate the X/Y/Z scan and feedback drive voltages (10 volts). Meanwhile, the AD7521 IC handles the DAC for the stick-slip sliding mechanism. Pmod headers carry SPI and control lines to and from the FPGA. As you can probably tell, this board was an absolute nightmare to design, and is the cause of many sleepless nights I will not get back.
3. **Scandrive**. Unrelated to the Spindrive from Project Hail Mary, although it has a similar name. The scandrive takes the output from the TIA and boosts it up to 40V to drive the four quadrants of the pizeo. Voltages applied in X and Y bend the disc for raster scanning; a voltage applied in Z sets the tip height by bending the whole disc inward, bringing the Pt-Ir tip with it.
4. **Sliderdrive**. This uses an FPGA to generate the sawtooth waveform for the stick-slip coarse approach algorithm, slowly walking the tip towards the sample when it's still millimeters out rather than nanometers before the fine tuning (Scandrive) takes over. Essentially, the waveform vibrates the tip at just the right frequency that it inches forwards a tiny amount (millimeters), then stops. It repeats, until a tiny tunneling current is detected; at those distances, the scandrive takes over fine approach and raster scanning by tilting the buzzer (see above).
5. **PSU**. All good things need power, and ATLAS is no exception. It runs on 15V - my original design called for a 45V rail to drive the tip movement for maximum range, but I decided against it for redundancy's sake - this project is already complicated enough without splitting 3 power rails (10, 15 and 45V).
### Damping
The PCBs were only one part of the challenge. A STM is an extremely sensitive instrument - after all, it's imaging individual atoms - even someone shouting next to it *will* throw the measurement off. To that end, ATLAS was built in one of the less used classrooms of Winchester College Mill, to keep foot traffic to a minimum; and a large sign was taped to the door telling people to keep their voices down. BUT THAT WASN'T ENOUGH! Any vibrations of the table would also throw the tip off by millimeters (matters a lot on the nanometer scale), so the whole system had to be on a damper.

The damper consists of a frame, 8 springs and a 12lb slab of granite, on which rests the scanner tip assembly. The frame was cut out of 6061 aluminium t-bar as a cuboid, and the granite base was suspended from the frame with the 8 springs. This gives the whole system a natural frequency of 1Hz, so it's not disturbed by any wind and/or noise. I briefly considered building an enclosure with ANC, but I ultimately decided against it - the last thing I need is another signal processing challenge. It would be fun though...
## Assembly
*The instructions provided below are but a summary, and your version of ATLAS will probably not work if you just follow these. For a more detailed set of instructions, or if you'd like to see how I did it, please refer to brentius.github.io/blog.*

A full bill of materials can be found at ```BOM.md```.
### Part I. The Scanner Block
This is the scanner block - i.e. the block that actually does the scanning. One of the main insights I lifted from OpenSTM was to use a buzzer and a stick-slip mechanism to slowly increment the position of the tip, which franly I think was an insight of genius. Why a buzzer? While your typical linear actuators and belt drives work for 3D printing or CNC milling, an STM requires nanometer precision, which you physically can't achieve with a linear actuator. There's also the problem that linear actuators produce heat, which at nanometer scales, really throws the position off due to the joints expanding/contracting. We first quarter the 
#### Preparing the tip
Version 1 of ATLAS used a length of 80:20 Pt-Ir (platinum-iridium) wire that I simply cut at 45 degrees with a pair of sharp cutters. Boring, but it works.
# Meta Stuff
## Acknowledgements
# References
