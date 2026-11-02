import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.*;
import org.semanticweb.owlapi.util.*;
import org.semanticweb.owlapi.io.RDFXMLOntologyFormat;
import com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory;
import java.io.File;
import java.util.*;

/** Setara Protégé "File > Export inferred axioms as ontology": asserted + inferred (class & property assertions). */
public class ExportInferred {
  public static void main(String[] a) throws Exception {
    OWLOntologyManager m = OWLManager.createOWLOntologyManager();
    OWLOntology o = m.loadOntologyFromOntologyDocument(new File(a[0]));
    OWLReasoner r = PelletReasonerFactory.getInstance().createReasoner(o);
    r.precomputeInferences(InferenceType.CLASS_ASSERTIONS, InferenceType.OBJECT_PROPERTY_ASSERTIONS, InferenceType.DATA_PROPERTY_ASSERTIONS);
    List<InferredAxiomGenerator<? extends OWLAxiom>> gens = new ArrayList<>();
    gens.add(new InferredClassAssertionAxiomGenerator());
    gens.add(new InferredPropertyAssertionGenerator());
    int before = o.getAxiomCount();
    new InferredOntologyGenerator(r, gens).fillOntology(m, o);
    System.out.println("Axioms before=" + before + " after=" + o.getAxiomCount() + " (inferred added=" + (o.getAxiomCount() - before) + ")");
    m.saveOntology(o, new RDFXMLOntologyFormat(), IRI.create(new File(a[1]).toURI()));
    System.out.println("Saved " + a[1]);
  }
}
