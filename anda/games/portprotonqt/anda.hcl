project pkg {
        arches = ["x86_64"]
	rpm {
		spec = "./portprotonqt.spec"
        
	}
	labels {
		mock = 1
	}
}